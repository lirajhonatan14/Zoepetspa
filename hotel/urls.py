from django.contrib import admin
from django.urls import path,include
from caixa import views as vw
from . import views
from hotel.views import nova_reserva
from django.views.generic import TemplateView


urlpatterns = [
        path('novareserva/', nova_reserva, name='reserva'), 
        path('novareservaday/', views.reservaday, name='reservaday'),
        path('lista_reservas/', views.reserva_list, name='lista_reserva'),
        path('lista_reservasday/', views.reservaday_list, name='lista_reservaday'),
        path('lista_reservabanho/', views.reservabanho_list, name='lista_reservabanho'),
        path('procurar_reserva/', views.puxar_reserva, name='puxar_reserva'),
        path('mostrar_reserva/<int:num_reserva>', views.mostrar_reserva, name='mostrar_reserva'),
        path('historico_reservas/', views.proc_reserva, name='historico_reserva'),
        path('procurar_reservaday/', views.puxar_reservaday, name='puxar_reservaday'),
        path('mostrar_reservaday/<int:num_reserva>  ', views.mostrar_reservaday, name='mostrar_reservaday'),
        path('mostrar_reservabanho/<int:num_reserva>  ', views.mostrar_reservabanho, name='mostrar_reservabanho'),
        path('renovar_pacote/', views.pacote, name='pacote'),
        path('pacote_renovado/', views.pacote_reservado, name='pacote_reservado'),
        path('reservar_banho/', views.reservar_banho, name='reservar_banho'),
        #path('calendario/', views.calendario, name='calendario'),
        path('calendario/', views.get_reservas, name='calendario'),

        
    ]
