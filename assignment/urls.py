from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('getTest',views.getTest,name='transition'),
    path('result',views.result,name='result')
]