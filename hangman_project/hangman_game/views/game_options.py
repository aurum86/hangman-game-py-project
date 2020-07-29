from django.shortcuts import render
from .main import get_post_response
from .. import game_options


g_game_options = game_options.GameOptions(difficulty_level=1)


def view_game_options(request):

    return render(
        request=request, template_name="hangman/game_options.html", context={}
    )


def save_options(request):
    global g_game_options

    __given_level = int(request.POST.get("difficulty_level", 1))
    g_game_options.difficulty_level = __given_level

    return get_post_response(view_name="hangman_game:hangman")
