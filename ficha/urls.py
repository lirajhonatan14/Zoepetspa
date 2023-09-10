from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'ficha'
urlpatterns = [
    path('novopet/', views.ficha, name='ficha'),
    path('listapet/', views.lista_fichas_cachorros, name='lista'),
    path('procurar_ficha/', views.puxar_ficha, name='puxar_ficha'),
    path('mostrar_ficha/<str:nome>', views.mostrar_ficha, name='mostrar_ficha'),
    path('cadastrar_vacina/', views.cadastrar_vacina, name='cadastrar_vacina'),
    path('selecionar_vacinas/', views.definir_vacina, name='definir_vacina'),
    path('vacina/', views.vacina, name='vacina'),
    path('proc_vacina/', views.proc_vacina, name='procvacina'),
    path('cadastrar_vacina/', views.cadastrar_vacina, name='cadastrar_vacina'),
    
    
    
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

