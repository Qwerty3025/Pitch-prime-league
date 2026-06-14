from django.urls import path
from . import views

app_name = 'matches'

urlpatterns = [
    path('fixtures/', views.fixture_list, name='fixture_list'),
    path('results/', views.result_list, name='result_list'),
    path('<int:pk>/', views.match_detail, name='match_detail'),
]
