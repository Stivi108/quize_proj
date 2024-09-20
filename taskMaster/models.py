from django.db import models
from django.utils.text import slugify

from users.models import Profile
# Create your models here.


class TeamList(models.Model):
    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = "Команды"

    teamSlug = models.SlugField(unique=True, null=True) # слаг для наименования комнаты чата с названием группы
    team = models.CharField(max_length=42, unique=True) # название группы
    member = models.ManyToManyField(Profile) #участник(и) группы
    points = models.PositiveSmallIntegerField(default=0, blank=True, null=True)

    reserved = models.BooleanField(default=False, blank=True, null=True) # учавствует ли уже в игре
    is_ready = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.team


class Question(models.Model):
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = "Вопросы"

    title = models.TextField(unique=True, max_length=42)
    topic = models.TextField(max_length=42)
    question = models.TextField(max_length=420)
    cost = models.SmallIntegerField(default=5, blank=True, null=True)

    def __str__(self):
        return self.title


class Answers(models.Model):
    class Meta:
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = "Ответы на вопросы"

    qID = models.ForeignKey(Question, on_delete=models.CASCADE)
    answerSets = models.TextField(max_length=70)

    def __str__(self):
        return f'Вариант ответа на вопрос {self.qID}'


class GameList(models.Model): # предполагается что игра будет не одна, и можно будет видеть список игр идущих и завершенных
    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = "Игры"

    gameNAME = models.CharField(unique=True, max_length=42) # Условное название для игры (может использовать ID)
    RLSlug = models.SlugField(unique=True, max_length=42, null=False)  # ()слаг для формирования адреса до конкретной игры /RSLug/TeamSLUG/
    status = models.BooleanField(default=False) # Cтатус активности игры (идет/не идет)
    winner = models.CharField(max_length=42, default='Не определён') #(после завершения заполняется команда победитель)

    def __str__(self):
        return self.gameNAME

    def save(self, *args, **kwargs):
        if not self.RLSlug:  # Проверяем, нужно ли генерировать slug
            self.RLSlug = slugify(self.gameNAME)
        super().save(*args, **kwargs)


class Round(models.Model):
    class Meta:
        verbose_name = 'Раунд'
        verbose_name_plural = "Раунды"

    game = models.ForeignKey(GameList, on_delete=models.CASCADE, to_field='gameNAME')
    round = models.PositiveIntegerField(default=1)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, to_field='title')

    def __str__(self):
        return f'Раунд №{self.round}'


class GameScore(models.Model):
    class Meta:
        verbose_name = 'Счет игры'
        verbose_name_plural = "Счеты игр"

    game = models.ForeignKey(GameList, on_delete=models.CASCADE, to_field='gameNAME')
    team = models.ForeignKey(TeamList, on_delete=models.CASCADE, to_field='team')

    current_round = models.SmallIntegerField(default=1)
    score = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"Счет команды {self.team.team} равен: {self.score}"


class RoundList(models.Model):
    class Meta:
        verbose_name = 'Сетка ответов'
        verbose_name_plural = "Сетки ответов"

    gameName = models.ForeignKey(GameList, on_delete=models.CASCADE, to_field='gameNAME') # по сути NameGame

    team = models.ForeignKey(TeamList, null=True, on_delete=models.CASCADE) #название команды
    round = models.PositiveIntegerField(default=1) # заголовок вопроса вопрос
    mark = models.IntegerField(default=0, null=True) # отметка о зачете ответа
    team_answer = models.CharField(max_length=70, null=True) # ответ от команды

    def __str__(self):
        return str(self.gameName.gameNAME)
