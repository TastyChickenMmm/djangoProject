from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('game/', views.game, name='game'),
    path('game_pending/', views.game_pending, name='game_pending'),
    path('profile/', views.profile, name='profile'),
]
