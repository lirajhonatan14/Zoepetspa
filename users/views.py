from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, user_passes_test

def acesso_negado(request):
    return render(request, 'acesso_negado.html')

@login_required(login_url="/auth/acesso_negado/")
def cadastro(request):
    if request.method == "GET":   
        return render(request,'cadastro.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        user = User.objects.filter(username=username).first()
        
        if user:
            return HttpResponse('Ja existe um usuario com esse nome')
        user = User.objects.create_user(username=username, email=email, password=senha) 
        user.save()
        return HttpResponse('Usuário cadastrado com sucesso')
    
def logindsd(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        
        user = authenticate(request,username=username, password=senha)
        if user:  
            auth_login(request, user)
            return HttpResponse('Autenticado')
        else:
            return HttpResponse('Email ou senha invalidos')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['senha']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'login.html')
    
