from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse


def get_post_response(view_name: str):
    return HttpResponseRedirect(reverse(viewname=view_name))


def redirect_view(request):
    return redirect("/hangman/")
