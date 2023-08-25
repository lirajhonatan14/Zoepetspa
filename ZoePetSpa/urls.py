from django.contrib import admin
from django.urls import path,include
from . import views

app_name="home"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('', include('ficha.urls')),
    path('', include('hotel.urls')),
    path('', include('caixa.urls')),
    path('logout/', views.logout_view, name='logout'), 
    path('', views.home, name='home'), 
    path('', include('calendario.urls')), 
    
]
