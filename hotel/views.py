from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import ReservaDayForm, Reservaform, ReservaBanhoForm
from datetime import datetime, date
from .models import Reserva, ReservaServicoAdicional, PacoteCliente
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Reserva, ReservaDay, ReservaBanho
from django.views.generic import View
from django.core.exceptions import ValidationError
from caixa.models import Caixa, CaixaDay, CaixaBanho


@login_required(login_url="/auth/login/")
# views.py
def nova_reserva(request):
    if request.method == 'POST':
        form_reserva = Reservaform(request.POST)
        if form_reserva.is_valid():
            reserva = form_reserva.save(commit=False)
            reserva.usuario = request.user
            reserva.save()
            form_reserva.save_m2m()
            return redirect('home')
    else:
        form_reserva = Reservaform()
    return render(request, 'reserva.html', {'form_reserva': form_reserva})





    
@login_required(login_url="/auth/login/")
def reservaday(request):
    if request.method == 'POST':
        form_reserva = ReservaDayForm(request.POST)
        
        if form_reserva.is_valid():
            reserva = form_reserva.save(commit=False)
            
            if reserva.pacote:
                pac = reserva.pacote
                quant = reserva.pacote.quantidade_dias
                nome = reserva.pet.nome
                
                # Verificar se já existe um pacote cliente para o cachorro e pacote selecionados
                pacote_cliente, created = PacoteCliente.objects.get_or_create(Dog=reserva.pet, pacote=pac, quantidade_dias = quant-1)
                
                pacote_cliente.save()
                
            reserva.usuario = request.user
            reserva.save()
            form_reserva.save_m2m()
            return redirect('home')
    else:
        form_reserva = ReservaDayForm()
    return render(request, 'reserva_day.html', {'form_reserva': form_reserva})

@login_required(login_url="/auth/login/")
def pacote(request):
    pacotes = PacoteCliente.objects.exclude(quantidade_dias=0)
    if request.method == 'POST':
        
        return redirect('mostrar_reserva')
        
    return render(request, 'pacote.html', {'pacotes': pacotes})

@login_required(login_url="/auth/login/")
def reserva_list(request):
    hoje = date.today()  # obtém a data atual
    reservas = Reserva.objects.filter(pago=False).order_by('data_entrada')

    context = {
        'reservas': reservas
    }
    return render(request, 'lista_reservas.html', context)

@login_required(login_url="/auth/login/")
def reservaday_list(request):
    hoje = date.today()  # obtém a data atual
    reservas = ReservaDay.objects.filter(pago=False).exclude(pacote__nome="Meia Diária/ Avaliação").order_by('data')
    avaliacao = ReservaDay.objects.filter(pago=False, pacote__nome='Meia Diária/ Avaliação').order_by('data')

    context = {
        'reservas': reservas,
        'avaliacao': avaliacao

    }
    return render(request, 'lista_reservasday.html', context)
@login_required(login_url="/auth/login/")
def reservabanho_list(request):
    reservas = ReservaBanho.objects.filter().order_by('data_reserva')
    
    
   
    context = {
        'reservas': reservas,
    
        
    }
    return render(request, 'lista_reservabanho.html', context)

@login_required(login_url="/auth/login/")
def proc_reserva(request):
    hoje = date.today()  # obtém a data atual
    reservas = Reserva.objects.all()
    reservasday = ReservaDay.objects.all()
    reservasbanho = ReservaBanho.objects.all()
    
    search = request.GET.get('search')
    if search:
        reservas = reservas.filter(pet__nome__icontains=search)
        reservasday = reservasday.filter(pet__nome__icontains=search)
        reservasbanho = reservasbanho.filter(cachorro__nome__icontains=search)
        
        
        

    context = {
        'reservas': reservas,
        'reservasday':reservasday,
        'reservasbanho':reservasbanho,
        
    }
    return render(request, 'historico_reserva.html', context)

@login_required(login_url="/auth/login/")
def puxar_reserva(request):
    if request.method == 'POST':
        return redirect('mostrar_reserva')
        
    animais = Reserva.objects.all()
    return render(request, 'procurar_reserva.html', {'animais': animais})

@login_required(login_url="/auth/login/")
def pacote_reservado(request):
    if request.method == 'POST':
        pacote_id = request.POST.get('dog_id')
        data = request.POST.get('data')
        hora = request.POST.get('hora_entrada')
        
        try:
           
            
            animal = ReservaDay.objects.get(pet_id=pacote_id, data__gte=date.today())
        except ReservaDay.DoesNotExist:
            # Lógica de tratamento caso a reserva não seja encontrada
            return HttpResponse("Reserva não encontrada")
        else:
            
            nova_reserva = ReservaDay()
            nova_reserva.pacote_id = animal.pacote_id
            nova_reserva.pet_id = animal.pet_id
            nova_reserva.usuario_id = request.user.id
            nova_reserva.data = data
            if animal.horario_personalizado:
                nova_reserva.horario_personalizado = animal.horario_personalizado
            if animal.instrucoes_medicamentos:
                nova_reserva.instrucoes_medicamentos = animal.instrucoes_medicamentos    
            if animal.horario_personalizado:
                nova_reserva.horario_personalizado = animal.horario_personalizado
            if animal.servicos_adicionais:
                nova_reserva.servicos_adicionais_id = animal.servicos_adicionais_id
            
            nova_reserva.horario_alimentacao = animal.horario_alimentacao
            nova_reserva.autorizacao_para_cuidados_medicos = animal.autorizacao_para_cuidados_medicos
            
            
            nova_reserva.hora_entrada = hora
            # Atribua outros campos conforme necessário
            
            # Salve a nova reserva
            nova_reserva.save()
            animal.delete()
            pacote_cliente = PacoteCliente.objects.get(Dog_id=pacote_id)
           
            pacote_cliente.quantidade_dias -= 1
            pacote_cliente.save()
            if pacote_cliente.quantidade_dias <= 0:
                pacote_cliente.delete()
                return redirect('home')
            

            return redirect('home')
    else:
        pacotes = PacoteCliente.objects.all()
        return redirect('home')
@login_required(login_url="/auth/login/")
def mostrar_reserva(request, num_reserva):
    try:
        animal = Reserva.objects.get(num_reserva=num_reserva)
        caixa = Caixa.objects.filter(num_reserva__num_reserva=num_reserva)
        
        if caixa:
            caixa = 0
    except Reserva.DoesNotExist:
        # Lógica de tratamento caso o animal não seja encontrado
        return HttpResponse("Reserva não encontrada")
    else:
        # Lógica para exibir a ficha do animal
        return render(request, 'mostrar_reserva.html', {'animal': animal, 'caixa':caixa})
@login_required(login_url="/auth/login/")   
def puxar_reservaday(request):
    if request.method == 'POST':
        return redirect('mostrar_reservaday')
        
    animais = ReservaDay.objects.all()
    return render(request, 'procurar_reservaday.html', {'animais': animais})


@login_required(login_url="/auth/login/")
def mostrar_reservaday(request, num_reserva):
    try:
        animal = ReservaDay.objects.get(num_reserva=num_reserva)
        nome = animal.pet.nome
        if animal.pacote:
            quant = PacoteCliente.objects.get(Dog__nome=nome)
        caixa = CaixaDay.objects.filter(num_reserva__num_reserva=num_reserva)
    except ReservaDay.DoesNotExist:
        # Lógica de tratamento caso o animal não seja encontrado
        return HttpResponse("Reserva não encontrada")
    else:
        # Lógica para exibir a ficha do animal
        return render(request, 'mostrar_reservaday.html', {'animal': animal, 'caixa':caixa, 'quant':quant})
    
@login_required(login_url="/auth/login/")
def mostrar_reservabanho(request, num_reserva):
    try:
        animal = ReservaBanho.objects.get(num_reserva=num_reserva)
        nome = animal.cachorro.nome
        caixa = CaixaBanho.objects.filter(num_reserva__num_reserva=num_reserva)
    except ReservaBanho.DoesNotExist:
        # Lógica de tratamento caso o animal não seja encontrado
        return HttpResponse("Reserva não encontrada")
    else:
        # Lógica para exibir a ficha do animal
        return render(request, 'mostrar_reservabanho.html', {'animal': animal, 'caixa':caixa})
    
     
@login_required(login_url="/auth/login/")
def pacotes(request):
    if request.method == 'POST':
        form_reserva = ReservaDayForm(request.POST)
        if form_reserva.is_valid():
            reserva = form_reserva.save(commit=False)
            reserva.usuario = request.user
            reserva.save()
            form_reserva.save_m2m()
            return redirect('home')
    else:
        form_reserva = ReservaDayForm()
    return render(request, 'pacote.html', {'form_reserva': form_reserva})

def reservar_banho(request):
    if request.method == 'POST':
        form = ReservaBanhoForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            form.save_m2m()
            reserva.save()
            return HttpResponse("Reserva feita com sucesso!")
        
    else:
        form = ReservaBanhoForm()
    
    context = {
        'form': form,
    }
    return render(request, 'reserva_banho.html', context)



