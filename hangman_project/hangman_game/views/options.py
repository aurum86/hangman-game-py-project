from django.shortcuts import render
from .main import get_post_response
from ..game import options
from ..game import progress
from .. import forms

g_game_options = options.GameOptions(
    difficulty=progress.DifficultyFactory.create_difficulty(difficulty_level=1),
    translate_word=True,
    target_language="en",
)


def view_game_options(request):
    return render(
        request=request,
        template_name="hangman/options.html",
        context={
            "form": forms.OptionsForm(
                data={
                    "difficulty_level": g_game_options.difficulty.difficulty_level,
                    "translate_word": g_game_options.translate_word,
                    "target_language": g_game_options.target_language,
                }
            )
        },
    )


def save_options(request):
    global g_game_options

    if request.method == "POST":
        __form = forms.OptionsForm(request.POST)
        if __form.is_valid():
            g_game_options.difficulty.difficulty_level = int(
                __form.cleaned_data["difficulty_level"]
            )
            g_game_options.translate_word = __form.cleaned_data["translate_word"]
            g_game_options.target_language = __form.cleaned_data["target_language"]

            return get_post_response(view_name="hangman_game:continue_game")
        else:
            return view_game_options(request)
