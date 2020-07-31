from django.shortcuts import render
from .main import get_post_response
from ..game import options
from .. import forms

g_game_options = options.GameOptions(difficulty_level=1)


def view_game_options(request):
    return render(
        request=request, template_name="hangman/options.html", context={
            "form": forms.OptionsForm(data={
                "difficulty_level": g_game_options.difficulty_level
            })
        }
    )


def save_options(request):
    global g_game_options

    if request.method == 'POST':
        __form = forms.OptionsForm(request.POST)
        if __form.is_valid():
            g_game_options.difficulty_level = int(__form.data["difficulty_level"])

            return get_post_response(view_name="hangman_game:hangman")
        else:
            return view_game_options(request)
