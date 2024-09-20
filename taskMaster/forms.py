from django import forms

from .models import *


class SendAnswerForm(forms.ModelForm):
    class Meta:
        model = RoundList
        fields = ['team_answer', ]

    team_answer = forms.CharField(max_length=42)


class CreateNewTeamForm(forms.ModelForm):
    class Meta:
        model = TeamList
        fields = ['team', "member"]

    team = forms.CharField(max_length=42,
                           label='Название')
    member = forms.CharField(max_length=420,
                           label='Участники'
                             )


class CreateNewGameForm(forms.ModelForm):
    class Meta:
        model = RoundList
        fields = ['gameName', 'team1', 'team2', 'team3', 'team4', 'team5', ]

    gameName = forms.CharField(max_length=42)

    choices = ((i, i.team) for i in TeamList.objects.filter(reserved=False))
    team1 = forms.ChoiceField(choices=choices)
    choices = ((i, i.team) for i in TeamList.objects.filter(reserved=False))
    team2 = forms.ChoiceField(choices=choices)
    choices = ((i, i.team) for i in TeamList.objects.filter(reserved=False))
    team3 = forms.ChoiceField(choices=choices)
    choices = ((i, i.team) for i in TeamList.objects.filter(reserved=False))
    team4 = forms.ChoiceField(choices=choices)
    choices = ((i, i.team) for i in TeamList.objects.filter(reserved=False))
    team5 = forms.ChoiceField(choices=choices)


class SelectGameForm(forms.ModelForm):
    pass
#     class Meta:
#         model = RoundList
#         fields = ['gameName', 'team1', 'team2', 'team3', 'team4', 'team5',]
#


class NewQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"

    title = forms.CharField(
        max_length=42,
        label='Заголовок вопроса:'
    )
    topic = forms.CharField(
        max_length=42,
        label='Тема вопроса:'
    )
    question = forms.CharField(
        max_length=420,
        label='Текст вопроса:'
    )
    cost = forms.IntegerField(
        max_value=30,
        min_value=5,
        label='Стоимость вопроса:'
    )

    answerSets = forms.CharField(
        max_length=70,
        label='Варианты ответа на вопросы:',

    )


class SelectQuestionForm(forms.ModelForm):
    class Meta:
        model = Round
        fields = ['question', 'round']

    def __init__(self, *args, gameName=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.gameName = gameName
        self.fields['question'] = forms.ChoiceField(
            label='Выберите вопрос',
            choices=self.get_question_choices()
        )
        # Устанавливаем значение по умолчанию для поля 'round'
        last_round = self.get_last_round()  # Получаем последний раунд
        if last_round is not None and last_round != 10: # настройки по количееству раундов пока не сделал
            self.fields['round'].initial = last_round + 1  # Увеличиваем на 1
        elif last_round is None:
            self.fields['round'].initial = 1

    def get_last_round(self):
        # Получаем последний раунд для данной игры
        game = GameList.objects.get(gameNAME=self.gameName)
        rounds = Round.objects.filter(game=game).order_by('round')
        if rounds.exists():
            return rounds.last().round  # Возвращаем последний раунд
        return None  # Если раундов нет, возвращаем None

    def get_question_choices(self):
        # Здесь фильтруем вопросы по game_id
        # Например, если у тебя есть модель Question
        all_questions = Question.objects.all()
        old_questions = [rQuest.question.title for rQuest in Round.objects.filter(game=self.gameName)]
        return [(newQ, newQ.title) for newQ in all_questions if newQ.title not in old_questions]

    round = forms.IntegerField(
        label='Выберите раунд',
        min_value=1,
        max_value=15,
        step_size=1
    )
