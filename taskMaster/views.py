from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from users.models import User
from .functions import is_unique
from .models import *
from .forms import SendAnswerForm, CreateNewTeamForm, CreateNewGameForm, SelectQuestionForm, SelectGameForm, \
    NewQuestionForm
from django.views.generic import *
from django.contrib import messages
# Create your views here.
from django.views import View


def next_round(request, round, game, team, url: str, url_fin: str = 'taskmaster:home'):
    next_round = int(round) + 1
    if Round.objects.filter(game=game, round=next_round).exists():
        # Если следующий раунд существует, перенаправляем на новый раунд
        return redirect(url, gameName=game, team=team, round=next_round)
    else:  # В противном случае команда завершает игру
        # all_rounds = set([r.round for r in Round.objects.filter(
        #     game=GameList.objects.get(gameNAME=game)
        # )])
        # team_rounds_completed = set([r.round for r in RoundList.objects.filter(
        #     gameName=GameList.objects.get(gameNAME=game),
        #     team=TeamList.objects.get(team=team)
        # )])
        # passed_rounds = list(all_rounds-team_rounds_completed)
        # if passed_rounds != []: #проверка на пропущенные раунды
        #     messages.error(request, 'Вы как то пропустили раунд! Можете его допройти!')
        #     return redirect(url, gameName=game, team=team, round=passed_rounds[0])
        messages.success(request, f"Успех! Все раунды успешно пройдены!.")
        return redirect(url_fin)


# class GetQuestionView(ListView):
#     model = Question
#     template_name = ''
#     context_object_name = 'question'
#
#     def get_queryset(self):
#         all_questions = Question.objects.all()
#         old_questions = RoundList.objects.all()
#
#         for newQ in all_questions:
#             if newQ not in old_questions:
#                 return newQ

class CreateNewTeamView(LoginRequiredMixin, FormView):
    form_class = CreateNewTeamForm
    template_name = 'taskmaster/create_team.html'

    def post(self, request, *args, **kwargs):
        team = request.POST.get('team')
        members_usernames = request.POST.get('member').split(',')
        members = []
        for username in members_usernames:
            username = username.strip()  # Удаляем пробелы
            try:
                user = User.objects.get(username=username)
                member_profile = Profile.objects.get(user=user)
                members.append(member_profile)
            except (User.DoesNotExist, Profile.DoesNotExist):
                messages.error(request, f"Пользователь '{username}' не найден.")
                return redirect('taskmaster:newteam')

        if TeamList.objects.filter(team=team).exists():
            messages.error(request, 'Команда с таким именем уже существует! Введите другое название!')
            return redirect('taskmaster:newteam')

            # Создание новой команды
        new_team = TeamList.objects.create(
            teamSlug=slugify(team),
            team=team,
        )

        # Добавление участников в команду
        new_team.member.set(members)  # Используем метод set для добавления нескольких профилей

        # Назначение лидера команды
        Profile.objects.filter(user=request.user).update(teamLead=True, team=new_team.team)
        messages.success(request, f"Создана команда '{team}'.")
        return redirect('taskmaster:home')


class CreateNewGameView(FormView):  # доступ только админам
    form_class = CreateNewGameForm
    template_name = 'taskmaster/create_game.html'

    def post(self, request, *args, **kwargs):
        gameN = request.POST.get('gameName')  # изъяли имя игры
        teamList = [TeamList.objects.get(team=request.POST.get(f'team{i}')) for i in range(1, 6)]
        if not is_unique(teamList):  # проверка уникальности выбранных команд
            messages.error(request, f"Ошибка! Команды не должны повторяться!.")
            return redirect('taskmaster:newgame')

        # проверка нет ли игры с таким названием
        if not GameList.objects.filter(gameNAME=gameN).exists():
            GameList.objects.create(
                gameNAME=gameN,
            )

            for team in teamList:
                GameScore.objects.create(
                    game=GameList.objects.get(gameNAME=gameN),
                    team=team,
                    current_round=1,
                    score=0
                )
            return redirect('taskmaster:selectanswer', gameN)
        else:
            return redirect('taskmaster:newgame')


class SelectAnswerView(FormView):
    form_class = SelectQuestionForm
    template_name = 'taskmaster/game/select_answer.html'

    def get_form_kwargs(self):
        # Получаем стандартные аргументы для формы
        kwargs = super().get_form_kwargs()
        # Добавляем game_id из URL или другого источника
        kwargs['gameName'] = self.kwargs['gameName']
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gameName'] = self.kwargs['gameName']  # Добавляем gameName в контекст
        game = GameList.objects.get(gameNAME=self.kwargs['gameName'])
        context['roundList'] = {r.round: r.question for r in Round.objects.filter(game=game)}
        return context

    def post(self, request, *args, **kwargs):
        gameName = GameList.objects.get(gameNAME=kwargs['gameName'])
        round = request.POST.get('round')
        quest = Question.objects.get(title=request.POST.get('question'))

        Round.objects.create(
            game=gameName,
            round=round,
            question=quest
        )
        round_count = Round.objects.filter(game=gameName).count()
        if round_count >= 10:
            messages.success(request, f"Успех! Все {round_count} раундов успешно созданы.")
            return redirect('taskmaster:home')  # Переход на следующую
        else:
            return redirect('taskmaster:selectanswer', gameName)


# class SendAnswerView(FormView): #устаревшее, переделано в GetQuestionPostAnswerView
#     form_class = SendAnswerForm
#     template_name = 'taskmaster/game/round_team.html'
#
#     def post(self, request, *args, **kwargs):
#         game = kwargs['gameName']
#         round = int(kwargs['round'])
#         tQuestion = Round.objects.get(game=game, round=round).question.title
#
#         team = kwargs['team']
#         correct = [a.lower().strip(',') for a in
#                    Answers.objects.get(qID=Question.objects.get(title=tQuestion).id).answerSets.split()]
#         answer = request.POST.get('team_answer')
#
#         mark = 0
#
#         if answer.lower() in correct:
#             mark = 5
#
#         if RoundList.objects.filter(
#                 gameName=GameList.objects.get(gameNAME=game),
#                 team=TeamList.objects.get(team=team),
#                 round=round
#         ).exists():
#             return HttpResponse('ОТвет в этом раунде уже был дан!')
#
#         RoundList.objects.create(
#
#             gameName=GameList.objects.get(gameNAME=game),
#             team=TeamList.objects.get(team=team),
#             round=round,
#             mark=mark,
#             team_answer=answer
#         )
#         game = GameList.objects.get(gameNAME=game)
#         team = TeamList.objects.get(team=team)
#         scoreObj = GameScore.objects.get_or_create(game=game, team=team)[0]
#
#         scoreObj.current_round = round
#         scoreObj.score += mark
#         scoreObj.save()
#
#         return HttpResponse(f"Оценка за задание: {mark}!")
# class GetQuestionView(DetailView):
#     template_name = 'base/master.html'
#
#     def get(self, request, *args, **kwargs):
#         game = kwargs['gameName']
#         round = int(kwargs['round'])
#         quest = Round.objects.get(game=game, round=round)
#         questTitle = quest.question.title
#         question = quest.question.question
#         # return JsonResponse({'questTitle': questTitle, 'question': question})
#         context = {
#             'questTitle': quest.question.title,
#             'question': quest.question.question
#         }
#         return render(request, self.template_name, context)


class GetAllGamesView(ListView):
    model = GameList
    template_name = 'base/game_list.html'
    context_object_name = 'games'

    def get(self, request):
        games = GameList.objects.all()  # Извлекаем все объекты из модели Game
        context = {'games': games}  # Формируем контекст
        return render(request, self.template_name, context)


class GameDetailView(DetailView):
    model = GameList
    template_name = 'base/game_detail.html'  # Шаблон для детали игры
    context_object_name = 'game'
    slug_field = 'RLSlug'
    slug_url_kwarg = 'slug'

    def get(self, request, slug):
        game = GameList.objects.get(RLSlug=slug)  # определяем игру по слагу в url
        gameScores = GameScore.objects.filter(game=game)
        # myteam = Profile.objects.get(user=request.user).team
        context = {'game': game, 'myteam': 'myteam', "teams": RoundList.objects.filter(gameName=game),
                   'gameScore': gameScores}  # Формируем контекст
        return render(request, self.template_name, context)


class GetQuestionPostAnswerView(View):
    template_name = 'taskmaster/game/round_team.html'
    form_class = SendAnswerForm

    def get(self, request, *args, **kwargs):
        # Получаем данные для отображения вопроса

        game = kwargs['gameName']
        round = int(kwargs['round'])

        quest = Round.objects.get(game=GameList.objects.get(gameNAME=game), round=round)
        questTitle = quest.question.title
        question = quest.question.question

        # Инициализируем форму для ответа
        form = self.form_class()

        context = {
            'room_name': kwargs['team'],
            'Round': round,
            'questTitle': questTitle,
            'question': question,
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Логика обработки ответа
        game = kwargs['gameName']
        team = kwargs['team']

        round = int(kwargs['round'])
        if team not in [team.team.team for team in RoundList.objects.filter(team=TeamList.objects.get(team=team))]:
            messages.error(request, 'Вы не участник выбранной игры!')
            return redirect('taskmaster:home')

        self.Question = Round.objects.get(game=game, round=round).question
        self.title_Q = self.Question.title
        self.question = self.Question.question
        context = {
            'game': game,
            'round': round,
            'team': team,
            'form': self.form_class()
        }

        correct = [a.lower().strip(',') for a in
                   Answers.objects.get(qID=Question.objects.get(title=self.title_Q).id).answerSets.split()]
        answer = request.POST.get('team_answer')

        mark = 0
        if answer.lower() in correct:
            mark = 5

        if RoundList.objects.filter(
                gameName=GameList.objects.get(gameNAME=game),
                team=TeamList.objects.get(team=team),
                round=round).exists():
            return next_round(
                request=request,
                round=round, team=team, game=game,
                url='taskmaster:gameprocess',

            )

        RoundList.objects.create(
            gameName=GameList.objects.get(gameNAME=game),
            team=TeamList.objects.get(team=team),
            round=round,
            mark=mark,
            team_answer=answer
        )
        gameObj = GameList.objects.get(gameNAME=game)
        teamObj = TeamList.objects.get(team=team)
        scoreObj = GameScore.objects.get_or_create(game=gameObj, team=teamObj)[0]

        scoreObj.current_round = round
        scoreObj.score += mark
        scoreObj.save()

        return next_round(
            request=request,
            round=round, team=team, game=game,
            url='taskmaster:gameprocess',

        )


class NewQuestionView(View):
    form_class = NewQuestionForm
    template_name = 'taskmaster/new_question.html'

    def get(self, request, *args, **kwargs):
        # Получаем данные для отображения вопросов
        questions = Question.objects.all()
        # Инициализируем форму для ответа
        form = self.form_class()

        context = {
            'questions': questions,
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        title = request.POST.get('title')
        topic = request.POST.get('topic')
        question = request.POST.get('question')
        cost = request.POST.get('cost')

        if title not in Question.objects.filter(title=title):
            question = Question.objects.create(
                title=title,
                topic=topic,
                question=question,
                cost=cost
            )
            answerSets = request.POST.get('answerSets')
            Answers.objects.create(
                qID=question,
                answerSets=answerSets
            )
            messages.success(request, 'Вопрос успешно добавлен')

            return redirect('taskmaster:newquestion')
        else:
            messages.error(request,
                           'Вопрос не должен повторяться!  Введите другой или убедитесь что вопрос который вы вводите не повторяется и введите другое название вопроса!')
            redirect('taskmaster:newquestion', request)

#########################################################################################
############ часть с началом игры ###############################


from django.http import JsonResponse


def check_ready_status(request, game_slug):
    game = GameList.objects.get(RLSlug=game_slug)
    teams = TeamList.objects.filter(reserved=False)
    ready_status = {team.team: team.is_ready for team in teams}
    return JsonResponse({'status': ready_status})


def lobby_view(request, game_slug):
    game = GameList.objects.get(RLSlug=game_slug)
    teams = TeamList.objects.filter(reserved=False)  # Берем только команды, резервированные для данной игры
    user_prof = Profile.objects.get(user=request.user)
    user_team = user_prof.team
    if request.method == "POST" and request.user.is_authenticated:

        if user_prof.team in [team.team for team in teams]:
            team = TeamList.objects.get(team=user_prof.team)  # получаем команду пользователя
            team.is_ready = True
            team.save()
        else:
            messages.error(request, 'Вы не участник этой игры!')
            return redirect('taskmaster:home')

    all_ready = all(team.is_ready for team in teams)  # Проверяем, готовы ли все команды

    if all_ready:
        # Здесь можно начать игру
        game.status = True
        game.save()
        # Переход к странице игры
        return redirect('taskmaster:gameprocess', gameName=game.gameNAME, team=user_team, round=1)


    return render(request, 'lobby.html', {'game': game,
                                          'teams': teams,
                                          'team': Profile.objects.get(user=request.user).team})


