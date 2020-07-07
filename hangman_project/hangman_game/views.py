from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpRequest
from .game import *
from .words import *


_word_length_range = (2, 3)
_secret_word = SecretWord(secret_word=get_random_word(_word_length_range))
_game_status = GameStatus(GameStatus.STATUS_BEGIN)
_hangman = Hangman(_secret_word, _game_status)
_knowledge = Knowledge(hangman=_hangman, known_word=None)


def _game_content(view_content: dict, word_with_mask: str, game_status: int) -> dict:
    view_content.update(
        {"word_with_mask": word_with_mask, "status_level": game_status,}
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
    # _game_status.reset()
    # _knowledge = Knowledge(hangman=_hangman, known_word=None)

    global _secret_word
    global _game_status
    global _hangman
    global _knowledge
    global _word_length_range

    _secret_word = SecretWord(secret_word=get_random_word(_word_length_range))
    _game_status = GameStatus(GameStatus.STATUS_BEGIN)
    _hangman = Hangman(_secret_word, _game_status)
    _knowledge = Knowledge(hangman=_hangman, known_word=None)

    return render(
        request=request,
        template_name="hangman/hangman.html",
        context=_game_content({}, _knowledge.get_word(), _hangman.get_game_status()),
    )


def guess_letter(request: HttpRequest):
    letter = request.POST["letter"]

    if len(letter) != 1:
        return validation_content(request, "You didn't provide a valid letter (must be one and only one).")

    letter = letter.lower()

    if not _hangman.is_game_finished():
        positions = _hangman.ask_for_letter(letter)
        _knowledge.set_letters(positions, letter)

    return render(
        request=request,
        template_name="hangman/hangman.html",
        context=_game_content(
            {
                "secret_word": _secret_word.get_word()
                if _hangman.is_game_finished()
                else None
            },
            _knowledge.get_word(),
            _hangman.get_game_status(),
        ),
    )


def guess_word(request):
    word = request.POST["word"]

    if len(word) == 0:
        return validation_content(request, "You didn't provide a word.")

    word = word.lower()

    if not _hangman.is_game_finished():
        _hangman.ask_for_word(word)

    return render(
        request=request,
        template_name="hangman/hangman.html",
        context=_game_content(
            {
                "secret_word": _secret_word.get_word()
                if _hangman.is_game_finished()
                else None
            },
            _knowledge.get_word(),
            _hangman.get_game_status(),
        ),
    )


def game_options(request):

    return render(
        request=request,
        template_name="hangman/game_options.html",
        context={}
    )


def validation_content(request, word__):
    return render(
        request=request,
        template_name="hangman/hangman.html",
        context=validation_error_content(
            _game_content({}, _knowledge.get_word(), _hangman.get_game_status()),
            word__,
        ),
    )
