from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import redirect, render
from ficha.models import FichaDog, VacinaAnimal
from datetime import datetime, timedelta

def logout_view(request):
    logout(request)
    return redirect('home')

from datetime import date
def verificar_vacina():
    vacinas_vencidas = []
    vacinas_reforco = []
    # Obtenha todos os objetos VacinaAnimal
    vacina_animal_objs = VacinaAnimal.objects.all()

    # Verifique a validade e a data de reforço das vacinas para cada objeto VacinaAnimal
    for vacina_animal in vacina_animal_objs:
        vacina = vacina_animal.vacina

        # Verifique se a vacina está vencida

        if vacina.validade <= date.today():
            vacinas_vencidas.append(vacina_animal)
            
        

        # Verifique se a vacina está no período de reforço
        if vacina.data_reforco and vacina.data_reforco <= date.today():
            vacinas_reforco.append(vacina_animal)
            
            
    return vacinas_vencidas, vacinas_reforco


def lembrardatanasc(mes):
     # Obtenha o número do mês atual
    mes_atual = datetime.now().month

    # Verifique se o mês fornecido é o mês atual ou futuro
    if mes >= mes_atual:
        # Filtrar os cachorros que fazem aniversário no mês fornecido
        cachorros_aniversario = FichaDog.objects.filter(data_de_nascimento__month=mes)
        return cachorros_aniversario
    else:
        return []
def home(request, mes=None):
    if mes is None:
        # Obtenha o mês atual
        mes = datetime.now().month
    proximo_mes = mes + 1 if mes < 12 else 1
    aniversario = FichaDog.objects.filter(data_de_nascimento__month=proximo_mes)
    animal = FichaDog.objects.all()
    usuario = request.user
    cachorros_aniversario = FichaDog.objects.filter(data_de_nascimento__month=mes)
    vacinas_vencidas, vacinas_reforco = verificar_vacina()
    vacinas_vencidas_info = []

# Lista para armazenar as informações das vacinas no período de reforço
    vacinas_reforco_info = []

    # Preenchendo as listas com as informações das vacinas
    for vacina_animal in vacinas_vencidas:
        vacina_info = {
            'animal_nome': vacina_animal.pet.nome,
            'animal_raca': vacina_animal.pet.raca,
            'vacina_nome': vacina_animal.vacina.nome,
            'data_validade': vacina_animal.vacina.validade,
            
        }
        vacinas_vencidas_info.append(vacina_info)

    for vacina_animal in vacinas_reforco:
        vacina_info = {
            'animal_nome': vacina_animal.pet.nome,
            'animal_raca': vacina_animal.pet.raca,
            'vacina_nome': vacina_animal.vacina.nome,
            'data_reforco': vacina_animal.vacina.data_reforco,
        }
        vacinas_reforco_info.append(vacina_info)

    # Adicione as listas de informações no contexto para exibir no template HTML
    
    if mes == 1:
        mesnome = 'Janeiro'
        proxmes = 'Fevereiro'
    elif mes == 2:
        mesnome = 'Fevereiro'
        proxmes = 'Março'
    elif mes == 3:
        mesnome = 'Março'
        proxmes = 'Abril'
    elif mes == 4:
        mesnome = 'Abril'
        proxmes = 'Maio'
    elif mes == 5:
        mesnome = 'Maio'
        proxmes = 'Junho'
    elif mes == 6:
        mesnome = 'Junho'
        proxmes = 'Julho'
    elif mes == 7:
        mesnome = 'Julho'
        proxmes = 'Agosto'
    elif mes == 8:
        mesnome = 'Agosto'
        proxmes = 'Setembro'
    elif mes == 9:
        mesnome = 'Setembro'
        proxmes = 'Outubro'
    elif mes == 10:
        mesnome = 'Outubro'
        proxmes = 'Novembro'
    elif mes == 11:
        mesnome = 'Novembro'
        proxmes = 'Dezembro'
    elif mes == 12:
        mesnome = 'Dezembro'
        proxmes = 'Janeiro'    
        proxmes = 'Fevereiro'
        proxmes = 'Fevereiro'
        
    context = {
        'vacinas_vencidas': vacinas_vencidas_info,
        'vacinas_reforco': vacinas_reforco_info,
        'cachorros_aniversario': cachorros_aniversario,
        'mes':mesnome,
        'proxmes':proxmes,
        'aniversario': aniversario,
        'usuario':usuario,
    }
    return render(request, 'home.html', context)  

