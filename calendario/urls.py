from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
     path('tela_inicial/', views.tela_inicial, name='tela_inicial'),
     path('all_events/', views.all_events, name='all_events'), 
     path('add_event/', views.add_event, name='add_event'), 
     path('update/', views.update, name='update'),
     path('remove/', views.remove, name='remove'),
]