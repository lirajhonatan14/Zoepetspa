from . import views
from django.urls import path,include

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('acesso_negado/', views.acesso_negado, name='acesso_negado'),

]
