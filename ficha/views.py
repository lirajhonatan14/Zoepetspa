from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import DogForm, VacinaForm, VacinaAnimalForm
from django.contrib import messages
from ficha.models import FichaDog, VacinaAnimal, Vacina
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
@login_required(login_url="/auth/login/")
def ficha(request):
    if request.method == 'POST':
        form = DogForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Salvo com sucesso')
            return redirect('reserva')

    else:
        form = DogForm()
    return render(request, 'ficha.html', {'form': form})


@login_required(login_url="/auth/login/")
def lista_fichas_cachorros(request):
    cachorros = FichaDog.objects.all().order_by('nome')
    search = request.GET.get('search') 
    if search:
        cachorros = cachorros.filter(nome__icontains=search) 
    return render(request, 'lista_pet.html', {'cachorros': cachorros})
@login_required(login_url="/auth/login/")
def puxar_ficha(request):
    if request.method == 'POST':
        return redirect('mostrar_ficha')
        
    animais = FichaDog.objects.all()
    return render(request, 'proc_ficha.html', {'animais': animais})


@login_required(login_url="/auth/login/")
def mostrar_ficha(request, nome):
    try:
        animal = FichaDog.objects.get(nome=nome)
        vacina = VacinaAnimal.objects.filter(pet=nome).all()
    except FichaDog.DoesNotExist:
        # Lógica de tratamento caso o animal não seja encontrado
        return HttpResponse("Animal não encontrado")
    else:
        # Lógica para exibir a ficha do animal
        return render(request, 'mostrar_ficha.html', {'animal': animal, 'vacina':vacina})
@login_required(login_url="/auth/login/")
def cadastrar_vacina(request):
    if request.method == 'POST':
        form = VacinaForm(request.POST)
        form.save()
        messages.success(request, 'Vacina cadastrada com sucesso.')
        return redirect('ficha:cadastrar_vacina')
    else:
        form = VacinaForm()
    messages.success(request, 'Vacina cadastrada com sucesso.')
    return render(request, 'cadastrar_vacina.html', {'form':form})
@login_required(login_url="/auth/login/")
def definir_vacina(request):
    if request.method == 'POST':
        form = VacinaAnimalForm(request.POST)
        form.save()
        messages.success(request, 'Cadastro realizado com sucesso.')
        return redirect('ficha:definir_vacina')
    else:
        form = VacinaAnimalForm()
    return render(request, 'definir_vacinas.html', {'form':form})
@login_required(login_url="/auth/login/")
def proc_vacina(request):
    if request.method == 'POST':
        return redirect('ficha:vacina')
        
    animais = FichaDog.objects.all()
    return render(request, 'proc_vacina.html', {'animais': animais})

@login_required(login_url="/auth/login/")
def vacina(request):
    nome_id = request.POST.get('nome_id')
    try:
        animal = VacinaAnimal.objects.filter(pet=nome_id).all()
        animais = FichaDog.objects.get(nome=nome_id)
        
        nome = animais.nome
    except VacinaAnimal.DoesNotExist:
        # Lógica de tratamento caso o animal não seja encontrado
        return HttpResponse("Vacinas não encontrada")
    else:
        # Lógica para exibir a ficha do animal
        return render(request, 'vacina.html', {'animal': animal, 'nome': nome})


def lembrete_vacina(nome):
    data_administracao = VacinaAnimal.objects.filter(pet=nome)
    data_validade = data_administracao.vacina.validade
    data_adm = data_administracao.data_administracao
    if data_validade > data_adm:
        print('Vacina Vencida!')
    return 
   