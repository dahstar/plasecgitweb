# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('add_credit/', views.add_credit, name='add_credit'),
]
