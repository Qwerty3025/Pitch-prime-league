from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('base/', views.base, name='base'),
    path('rules/', views.rules, name='rules'),
    path('contact/', views.contact, name='contact'),
]
