from django.urls import path

from .views import main
from .views import game
from .views import options

app_name = "hangman_game"

urlpatterns = [
    path("", main.redirect_view, name="hangman_home"),
    path("hangman/", game.hangman, name="hangman"),
    path("guess_letter", game.guess_letter, name="guess_letter"),
    path("guess_word", game.guess_word, name="guess_word"),
    path("game_options", options.view_game_options, name="game_options"),
    path("hangman/game_options", options.view_game_options, name="game_options"),
    path("save_options", options.save_options, name="save_options"),
    path("hangman/save_options", options.save_options, name="save_options"),
]
