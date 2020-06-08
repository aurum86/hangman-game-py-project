from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpRequest


g_word_with_mask = '*******'
g_game_status = 0


def redirect_view(request):
    return redirect('/hangman/')


def game_content(view_content: dict, word_with_mask: str, game_status: int) -> dict:
    view_content.update({
        'word_with_mask': word_with_mask,
        'status_level': game_status,
    })
    return view_content


def validation_error_content(page_content: dict, error_message: str):
    page_content.update({
        'error_message': error_message,
    })
    return page_content


def hangman(request):
    return render(request=request, template_name='hangman/hangman.html', context=game_content(
        {},
        g_word_with_mask,
        g_game_status
    ))


def guess_letter(request: HttpRequest):
    letter = request.POST['letter']

    if len(letter) != 1:
        return render(
            request=request,
            template_name='hangman/hangman.html',
            context=validation_error_content(
                game_content({}, g_word_with_mask, g_game_status),
                "You didn't provide a valid letter (must be one and only one)."
            )
        )

    return render(request=request, template_name='hangman/hangman.html', context=game_content(
        {},
        g_word_with_mask,
        g_game_status
    ))


def guess_word(request):
    word = request.POST['word']

    if len(word) == 0:
        return render(
            request=request,
            template_name='hangman/hangman.html',
            context=validation_error_content(
                game_content({}, g_word_with_mask, g_game_status),
                "You didn't provide a word."
            )
        )

    return render(request=request, template_name='hangman/hangman.html', context=game_content(
        {},
        g_word_with_mask,
        g_game_status
    ))
