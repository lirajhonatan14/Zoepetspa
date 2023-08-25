from django.contrib.auth import logout
from django.shortcuts import redirect, render
from ficha.models import FichaDog, VacinaAnimal
from datetime import datetime, timedelta

def logout_view(request):
    logout(request)
    return redirect('home')

from datetime import date
def verificar_vacina():
    vacinas_vencidas = []
    validade = []
    
    vacina_animal_objs = VacinaAnimal.objects.all()
    for vacina_animal in vacina_animal_objs:
        vacina = vacina_animal.vacina

        proxima_dose = vacina_animal.data_administracao + timedelta(days=vacina.nova_dose)

        if proxima_dose <= date.today():
            vacinas_vencidas.append(vacina_animal)
            validade.append(proxima_dose.strftime('%d/%m/%Y'))  # Formata a data como string
   
    return vacinas_vencidas, validade


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
    vacinas_vencidas, validade = verificar_vacina()
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
        'validade': validade,
        'cachorros_aniversario': cachorros_aniversario,
        'mes':mesnome,
        'proxmes':proxmes,
        'aniversario': aniversario,
        'usuario':usuario,
    }
    return render(request, 'home.html', context)  

