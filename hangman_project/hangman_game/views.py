from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpRequest
from . import game
from . import words
from . import game_options


g_game_options = game_options.GameOptions(1)
_word_length_range = (g_game_options.get_word_length_min(), g_game_options.get_word_length_max())
g_secret_word = game.SecretWordFactory(words).create_secret_word(_word_length_range)
g_convict = game.ConvictFactory.create_convict(g_secret_word)


def _game_content(view_content: dict, word_with_mask: str, game_status: int) -> dict:
    view_content.update(
        {
            "word_with_mask": word_with_mask,
            "status_level": game_status,
        }
    )

    return view_content


def redirect_view(request):
    return redirect("/hangman/")


def validation_error_content(page_content: dict, error_message: str):
    page_content.update(
        {"error_message": error_message,}
    )
    return page_content


def hangman(request):

    global g_secret_word
    global g_convict

    _word_length_range = (g_game_options.get_word_length_min(), g_game_options.get_word_length_max())
    g_secret_word = game.SecretWordFactory(words).create_secret_word(_word_length_range)

    g_convict = game.ConvictFactory.create_convict(g_secret_word)

    return render(
        request=request,
        template_name="hangman/hangman.html",
        context=_game_content({}, g_convict.get_known_word(), g_convict.get_game_status()),
    )


def guess_letter(request: HttpRequest):
    letter = request.POST["letter"]
    letter = letter.lower()

    if len(letter) != 1:
        return validation_content(request, "You didn't provide a valid letter (must be one and only one).")

    if g_convict.is_game_finished():
        return validation_content(request, "Game is already over.")

    _is_correct = g_convict.guess_letter(letter)

    return render(
        request=request,
        template_name="hangman/hangman.html",
        context=_game_content(
            {
                "secret_word": g_secret_word.get_word() if g_convict.is_game_finished() else None,
                "is_game_finished": g_convict.is_game_finished(),
                "is_correct": _is_correct
            },
            g_convict.get_known_word(),
            g_convict.get_game_status(),
        ),
    )


def guess_word(request):
    _word = request.POST["word"]
    _word = _word.lower()

    if len(_word) == 0:
        return validation_content(request, "You didn't provide a word.")

    if g_convict.is_game_finished():
        return validation_content(request, "Game is already over.")

    _is_correct = g_convict.guess_word(_word)

    return render(
        request=request,
        template_name="hangman/hangman.html",
        context=_game_content(
            {
                "secret_word": g_secret_word.get_word() if g_convict.is_game_finished() else None,
                "is_game_finished": g_convict.is_game_finished(),
                "is_correct": _is_correct,
            },
            g_convict.get_known_word(),
            g_convict.get_game_status(),
        ),
    )


def view_game_options(request):

    return render(
        request=request,
        template_name="hangman/game_options.html",
        context={}
    )


def save_options(request):
    global g_game_options

    _given_level = int(request.POST.get("difficulty_level", 1))
    g_game_options.difficulty_level = _given_level

    return redirect_view(request)


def validation_content(request, validation_message):
    return render(
        request=request,
        template_name="hangman/hangman.html",
        context=validation_error_content(
            _game_content({}, g_convict.get_known_word(), g_convict.get_game_status()),
            validation_message,
        ),
    )
