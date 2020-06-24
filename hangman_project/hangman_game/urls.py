from django.urls import path

from . import views

app_name = "hangman_game"

urlpatterns = [
    path("", views.redirect_view, name="hangman-home"),
    path("hangman/", views.hangman, name="hangman"),
    path("guess_letter", views.guess_letter, name="guess_letter"),
    path("guess_word", views.guess_word, name="guess_word"),
]
