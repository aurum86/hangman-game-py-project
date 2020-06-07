from django.urls import path

from . import views

urlpatterns = [
    path('', views.redirect_view, name='hangman'),
    path('hangman/', views.index, name='hangman'),
]
