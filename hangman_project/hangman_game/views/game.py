from django.shortcuts import render
from django.http import HttpRequest
from ..game import game
from ..words import WordProvider
from .options import g_game_options
from ..game import statistics
from ..game import progress
from django.views import generic
from django.http import response
import collections


class KnownWordPrinter:
    """Prints known word"""

    __UNKNOWN_CHAR = "*"

    def __init__(self, convict: game.Convict, secret_word: game.SecretWord):
        self.__convict = convict
        self.__secret_word = secret_word

    def get_known_word(self) -> str:
        __known_word = collections.defaultdict(lambda: self.__UNKNOWN_CHAR)
        __known_word.update(self.__convict.get_known_letter_positions())

        __word_length = self.__secret_word.get_length()

        return "".join(
            [__known_word[__position] for __position in range(0, __word_length)]
        )


def create_progress() -> progress.Progress:
    return progress.ProgressFactory.create_progress(
        level=g_game_options.difficulty.difficulty_level
    )


g_progress = create_progress()

g_wordProvider = WordProvider()
__word_length_range = (
    g_game_options.difficulty.get_word_length_min(),
    g_game_options.difficulty.get_word_length_max(),
)

g_secret_word = game.SecretWordFactory(g_wordProvider).create_secret_word(
    word_length_range=__word_length_range
)
g_convict = game.ConvictFactory.create_convict(secret_word=g_secret_word)

g_known_word_printer = KnownWordPrinter(convict=g_convict, secret_word=g_secret_word)
g_guess_history = statistics.GuessHistory()


def __game_content(
    view_content: dict, word_with_mask: str, game_status: int, guess_history: list
) -> dict:
    view_content.update(
        {
            "word_with_mask": word_with_mask,
            "status_level": game_status,
            "guess_history": guess_history,
            "options": g_game_options,
            "progress": g_progress,
        }
    )

    return view_content


def validation_error_content(page_content: dict, error_message: str):
    page_content.update(
        {"error_message": error_message,}
    )
    return page_content


def continue_game(request):
    global g_progress

    g_progress = create_progress()

    return hangman(request)


def hangman(request):
    if not request.method == "GET":
        return response.HttpResponseNotAllowed(request.method)

    global g_secret_word
    global g_convict
    global g_known_word_printer
    global g_guess_history

    g_progress.evaluate_game_level()
    __difficulty = progress.DifficultyFactory.create_difficulty(
        g_progress.get_game_level()
    )

    __word_length_range = (
        __difficulty.get_word_length_min(),
        __difficulty.get_word_length_max(),
    )
    g_secret_word = game.SecretWordFactory(
        word_provider=g_wordProvider
    ).create_secret_word(word_length_range=__word_length_range)

    g_convict = game.ConvictFactory.create_convict(secret_word=g_secret_word)
    g_known_word_printer = KnownWordPrinter(
        convict=g_convict, secret_word=g_secret_word
    )
    g_guess_history = statistics.GuessHistory()

    return render(
        request=request,
        template_name="hangman/hangman.html",
        context=__game_content(
            {},
            g_known_word_printer.get_known_word(),
            g_convict.get_game_status(),
            g_guess_history.get_history(),
        ),
    )


def guess_letter(request: HttpRequest):
    if not request.method == "POST":
        return response.HttpResponseNotAllowed(request.method)

    letter = request.POST["letter"]
    letter = letter.lower()

    if len(letter) != 1:
        return validation_content(
            request, "You didn't provide a valid letter (must be one and only one)."
        )

    if g_convict.is_game_finished():
        return validation_content(request, "Game is already over.")

    __is_correct = g_convict.guess_letter(letter)
    g_guess_history.add_guess(letter)

    if g_convict.is_game_finished():
        g_progress.game_history.add_game_result(__is_correct)

    # TODO: use redirect here
    return render(
        request=request,
        template_name="hangman/hangman.html",
        context=__game_content(
            {
                "secret_word": g_secret_word.get_word()
                if g_convict.is_game_finished()
                else None,
                "is_game_finished": g_convict.is_game_finished(),
                "is_correct": __is_correct,
            },
            g_known_word_printer.get_known_word(),
            g_convict.get_game_status(),
            g_guess_history.get_history(),
        ),
    )


class GamePlay(generic.TemplateView):
    template_name = "hangman/hangman.html"

    def get(self, request, *args, **kwargs):
        return (super().get(request, {}),)


def guess_word(request):
    if not request.method == "POST":
        return response.HttpResponseNotAllowed(request.method)

    __word = request.POST["word"]
    __word = __word.lower()

    if len(__word) == 0:
        return validation_content(request, "You didn't provide a word.")

    if g_convict.is_game_finished():
        return validation_content(request, "Game is already over.")

    __is_correct = g_convict.guess_word(__word)
    g_guess_history.add_guess(__word)

    if g_convict.is_game_finished():
        g_progress.game_history.add_game_result(__is_correct)

    # TODO: use redirect here
    return render(
        request=request,
        template_name="hangman/hangman.html",
        context=__game_content(
            {
                "secret_word": g_secret_word.get_word()
                if g_convict.is_game_finished()
                else None,
                "is_game_finished": g_convict.is_game_finished(),
                "is_correct": __is_correct,
            },
            g_known_word_printer.get_known_word(),
            g_convict.get_game_status(),
            g_guess_history.get_history(),
        ),
    )


def validation_content(request, validation_message):
    return render(
        request=request,
        template_name="hangman/hangman.html",
        context=validation_error_content(
            __game_content(
                {},
                g_known_word_printer.get_known_word(),
                g_convict.get_game_status(),
                g_guess_history.get_history(),
            ),
            validation_message,
        ),
    )
