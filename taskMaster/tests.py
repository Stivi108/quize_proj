вобщем помогай. я не успеваю.
есть модель команд в джанго проекте:
class TeamList(models.Model):
    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = "Команды"

    teamSlug = models.SlugField(unique=True, null=True) # слаг для наименования комнаты чата с названием группы
    team = models.CharField(max_length=42, unique=True) # название группы
    member = models.ManyToManyField(Profile) #участник(и) группы
    points = models.PositiveSmallIntegerField(default=0, blank=True, null=True)

    is_ready = models.BooleanField(default=False, blank=True, null=True)  # флаг готовности к игре
    def str(self):
        return self.team

модель игр:
class GameList(models.Model): # предполагается что игра будет не одна, и можно будет видеть список игр идущих и завершенных
    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = "Игры"

    gameNAME = models.CharField(unique=True, max_length=42) # Условное название для игры (может использовать ID)
    RLSlug = models.SlugField(unique=True, max_length=42, null=False)  # ()слаг для формирования адреса до конкретной игры /RSLug/TeamSLUG/
    status = models.BooleanField(default=False) # Cтатус активности игры (идет/не идет)
    winner = models.CharField(max_length=42, default='Не определён') #(после завершения заполняется команда победитель)

нужно решение, для определения старта игры. хочу сделать примерно следующее: чтобы войти в не начатую игру, игроки переходили в некоторое лобби, где только лидер команды, сможет нажать на кнопку "готов" чтобы обозначить что команда готова, 
проблема в том что я не знаю как сделать автоматическое отслеживание готовности всех команд и дальнейший переход на непосредственное начало игры. это же можно сделать джава скриптами? я в них слаб, сам не придумаю, а нужно побыстрее приделать хотя бы этот функционал. вцелом он основной для проекта, функционал по отправки и фиксации ответов уже написан, нужно именно прописать лобби-старт игры. 
сможешь подсказать?