from django.urls import path
from . import views

app_name = 'league'

urlpatterns = [
    path('', views.season_list, name='season_list'),
    path('standings/<int:season_id>/', views.standings_table, name='standings_table'),
    path('teams/', views.team, name='team'),
    path('teams/<int:pk>/', views.team_detail, name='team_detail'),
    path('players/<int:pk>/', views.player_detail, name='player_detail'),
    
]
