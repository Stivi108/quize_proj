from django.urls import path

from .views import *

# taskmaster основное приложение приложение для реализации игры

urlpatterns = [
    path("home/", GetAllGamesView.as_view(), name='home'),
    path('games/<slug:slug>/', GameDetailView.as_view(), name='detail'),
    path("createNewTeam/", CreateNewTeamView.as_view(), name="newteam"),
    path("createNewGame/", CreateNewGameView.as_view(), name="newgame"), # создание игры
    path("selectAnswer/<gameName>", SelectAnswerView.as_view(), name="selectanswer"),  # выбор вопросов для созданой игры
    path("<gameName>/<team>/<round>/sendanswer/", GetQuestionPostAnswerView.as_view(), name="gameprocess"),
    path("question/add/", NewQuestionView.as_view(), name="newquestion"),

    path('lobby/<slug:game_slug>/', lobby_view, name='lobby'),
    path('lobby/<slug:game_slug>/status/', check_ready_status, name='check_ready_status'),

    ]
