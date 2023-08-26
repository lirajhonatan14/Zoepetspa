from django.http import HttpResponse, HttpResponseServerError
from django.contrib import messages
from hotel.models import Reserva, ReservaDay, PacoteCliente, ReservaBanho
from django.shortcuts import render, get_object_or_404,redirect
from .models import Caixa, CaixaDay, CaixaBanho
from .forms import CaixaForm, CaixaDayForm, CaixaBanhoForm
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from io import BytesIO
from django.urls import reverse
from django.utils import timezone
from django.template.loader import get_template
from xhtml2pdf import pisa
import io
from ficha.models import FichaDog
from datetime import timedelta, datetime
from django.db.models import Sum
from datetime import date
from decimal import Decimal


@login_required(login_url="/auth/login/")
def relatorios(request):
    if request.method == 'POST':
        mes = request.POST.get('mes')
        ano = request.POST.get('ano')
        tipo_reserva = request.POST.get('tipo_reserva')

        if tipo_reserva == 'hotel':
        # Fazendo a consulta para filtrar os itens da tabela Caixa
            caixas_filtrados = Caixa.objects.filter(data__month=mes, data__year=ano).order_by('data')
            valor_total = Caixa.objects.filter(data__month=mes, data__year=ano).aggregate(total=Sum('total'))['total']
            context = {
            'caixas_filtrados': caixas_filtrados,
            'valor_total':valor_total,
            }
            
            template_path = 'relatorio_vendas.html'
            template = get_template(template_path)
            html = template.render(context)

            # Create a BytesIO buffer to receive the PDF output
            buffer = io.BytesIO()

            # Generate the PDF output using the BytesIO buffer
            pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), buffer)

            # Return the PDF as an HTTP response
            response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = 'filename="relatorio_caixa.pdf"'
            return response
        
        elif tipo_reserva == 'day_care':
            caixas_filtrados = CaixaDay.objects.filter(data__month=mes, data__year=ano).order_by('data')
            valor_total = CaixaDay.objects.filter(data__month=mes, data__year=ano).aggregate(total=Sum('total'))['total']


            context = {
            'caixas_filtrados': caixas_filtrados,
            'valor_total':valor_total,
            }
            
            template_path = 'relatorio_vendas_day.html'
            template = get_template(template_path)
            html = template.render(context)

            # Create a BytesIO buffer to receive the PDF output
            buffer = io.BytesIO()

            # Generate the PDF output using the BytesIO buffer
            pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), buffer)

            # Return the PDF as an HTTP response
            response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = 'filename="relatorio_caixa_day.pdf"'
            return response
        elif tipo_reserva == 'banho':
            caixas_filtrados = ReservaBanho.objects.filter(data_reserva__month=mes, data_reserva__year=ano).order_by('data_reserva')
            valor_total = ReservaBanho.objects.filter(data_reserva__month=mes, data_reserva__year=ano).aggregate(total=Sum('total'))['total']
            context = {
            'caixas_filtrados': caixas_filtrados,
            'valor_total':valor_total,
            }
            
            template_path = 'relatorio_vendas_banho.html'
            template = get_template(template_path)
            html = template.render(context)

            # Create a BytesIO buffer to receive the PDF output
            buffer = io.BytesIO()

            # Generate the PDF output using the BytesIO buffer
            pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), buffer)

            # Return the PDF as an HTTP response
            response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = 'filename="relatorio_caixa_banho.pdf"'
            return response 
        
    
    return render(request, 'relatorios.html')

def total(reserva, num_reserva):
    caixa = Caixa.objects.filter(num_reserva=num_reserva)
    caixas = CaixaDay.objects.filter(num_reserva=num_reserva)
    # Lógica para calcular o total
    servicos_adicionais = caixa.num_reserva.servicos_adicionais
    if servicos_adicionais is not None and servicos_adicionais.valor_servico is not None:
        # O objeto servicos_adicionais e o atributo valor_servico estão definidos
        serv = servicos_adicionais.valor_servico
    else:
        # O objeto servicos_adicionais ou o atributo valor_servico é nulo
        serv = 0  # Ou qualquer outro valor padrão que você queira atribuir
    val = calcular_total(reserva)
    desc = caixa.desconto
    desc = (desc/100)*val
    total = (val-desc)+serv
    return total  # Valor do total calculado

@login_required(login_url="/auth/login/")
def caixa_hotel(request, num_reserva):
    reserva = Reserva.objects.get(num_reserva=num_reserva)
    usuario = request.user.username
    data_atual = date.today()

    # Convertendo para string no formato ISO (YYYY-MM-DD)
    data_str = data_atual.strftime('%d-%m-%Y')

    # Usando a string para criar um objeto Caixa
    caixa = Caixa(data=data_str)

    # Salvando o objeto Caixa no banco de dados
    
    if request.method == 'POST':
        caixa_form = CaixaForm(request.POST)
        reserva.pago = True
        reserva.save()
        if caixa_form.is_valid():
            # Get the cleaned form data
            cleaned_data = caixa_form.cleaned_data
            
            # Get the pet associated with the reservation
            pet = reserva.pet
            
            # Calculate the total value
            # Create a new Caixa object using the form data, pet, and total
            caixa = Caixa.objects.create(
                num_reserva=reserva,
                usuario=usuario,
                pet=pet,
                relatorio_estadia=cleaned_data['relatorio_estadia'],
                desconto=cleaned_data['desconto'],
                metodo_de_pagamento=cleaned_data['metodo_de_pagamento'],
                total=0
            )
            caixa.save()
            
            return redirect('caixa:relatorio', num_reserva=num_reserva)
        else:
            # Print out the form data and validation errors
            print(caixa_form.cleaned_data)
            print(caixa_form.errors)
    else:
        caixa_form = CaixaForm()
    
    context = {
        'reserva': reserva,
        'usuario': usuario,
        'caixa_form': caixa_form,
    }
    return render(request, 'caixa.html', context)




@login_required(login_url="/auth/login/")
def caixa_day(request, num_reserva):
    reserva = ReservaDay.objects.get(num_reserva=num_reserva)
    nome = reserva.pet_id
    
    usuario = request.user.username
    
    if request.method == 'POST':
        caixa_form = CaixaDayForm(request.POST)
        reserva.pago = True
        reserva.save()
        if caixa_form.is_valid():
            # Get the cleaned form data
            cleaned_data = caixa_form.cleaned_data
            
            # Get the pet associated with the reservation
            pet = reserva.pet
            
            # Create a new Caixa object using the form data and pet
            caixa = CaixaDay.objects.create(
                num_reserva=reserva,
                usuario=usuario,
                pet=pet,
                relatorio_estadia=cleaned_data['relatorio_estadia'],
                desconto=cleaned_data['desconto'],
                metodo_de_pagamento=cleaned_data['metodo_de_pagamento'],
                total=0
            )
            
            return redirect('caixa:relatorioday', num_reserva=num_reserva)
        else:
            # Print out the form data and validation errors
            print(caixa_form.cleaned_data)
            print(caixa_form.errors)
    else:
        caixa_form = CaixaForm()
    
    context = {
        'reserva': reserva,
        'usuario': usuario,
        'caixa_form': caixa_form,
    }
    return  render(request, 'caixa_day.html', context)
@login_required(login_url="/auth/login/")
def caixa_banho(request, num_reserva):
    reserva = ReservaBanho.objects.get(num_reserva=num_reserva)

    usuario = request.user.username
    
    if request.method == 'POST':
        caixa_form = CaixaBanhoForm(request.POST)
        reserva.status_de_pagamento = True
        reserva.save()
        if caixa_form.is_valid():
            # Get the cleaned form data
            cleaned_data = caixa_form.cleaned_data
            
            # Get the pet associated with the reservation
            pet = reserva.cachorro
            banhista = reserva.banhista
            # Create a new Caixa object using the form data and pet
            caixa = CaixaBanho.objects.create(
                num_reserva=reserva,
                banhista=banhista,
                pet=pet,
                relatorio_estadia=cleaned_data['relatorio_estadia'],
                desconto=cleaned_data['desconto'],
                metodo_de_pagamento=cleaned_data['metodo_de_pagamento'],
                total=0
            )
            
            return redirect('caixa:relatoriobanho', num_reserva=num_reserva)
        else:
            # Print out the form data and validation errors
            print(caixa_form.cleaned_data)
            print(caixa_form.errors)
    else:
        caixa_form = CaixaBanhoForm()
    
    context = {
        'reserva': reserva,
        'usuario': usuario,
        'caixa_form': caixa_form,
    }
    return  render(request, 'caixa_banho.html', context)

def diminuir_horas(tempo, horas):
    dt_tempo = datetime.combine(timezone.now().date(), tempo)
    dt_novo = dt_tempo - timedelta(hours=horas)
    tempo_novo = dt_novo.time()
    return tempo_novo
@login_required(login_url="/auth/login/")
def relatorio_reservas(request, num_reserva):
    # Get the Caixa objects for the given num_reserva
    caixas = Caixa.objects.filter(num_reserva=num_reserva)
    hora = timezone.now().time()
    hora_atual = diminuir_horas(hora, 3)

    
    # Create a list to hold the data for each Caixa object
    context_list = []

    # Loop through the queryset and create a dictionary for each Caixa object
    for caixa in caixas:
        # Get the Reserva and Pet objects associated with the Caixa object
        reserva = caixa.num_reserva
        pet = caixa.pet
        desc = caixa.desconto
        servicos_adicionais = caixa.num_reserva.servicos_adicionais

    if servicos_adicionais is not None and servicos_adicionais.valor_servico is not None:
        # O objeto servicos_adicionais e o atributo valor_servico estão definidos
        serv = servicos_adicionais.valor_servico
    else:
        # O objeto servicos_adicionais ou o atributo valor_servico é nulo
        serv = 0  # Ou qualquer outro valor padrão que você queira atribuir
    val = calcular_total(reserva)
    
    
   

    desc = (desc / 100) * val
    total = (val-desc)+serv
    caixa.total = total
    caixa.save()

        # Create a dictionary to hold the data for the PDF
    context = {
        'total': total,
        'hora_atual':hora_atual,
        'reserva': reserva,
        'num_reserva': reserva.num_reserva,
        'nome_pet': pet.nome,
        'nome_tutor': pet.nome_tutor,
        'cpf_tutor': pet.cpf_tutor,
        'data_entrada': reserva.data_entrada,
        'hora_entrada': reserva.hora_entrada,
        'data_saida': reserva.data_saida,
        'usuario': reserva.usuario,
        'relatorio':caixa.relatorio_estadia,
        'desconto':caixa.desconto,
        'servicos':servicos_adicionais,
        'metodo':caixa.metodo_de_pagamento,

        
    }

    context_list.append(context)

    # Render the PDF template with the context data
    template_path = 'relatorio_reservas.html'
    template = get_template(template_path)
    html = template.render({'context_list': context_list})

    # Create a BytesIO buffer to receive the PDF output
    buffer = io.BytesIO()

    # Generate the PDF output using the BytesIO buffer
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), buffer)

    # Return the PDF as an HTTP response
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'filename="relatorio_reservas.pdf"'
    return response
@login_required(login_url="/auth/login/")
def relatorio_reservasday(request, num_reserva):
    caixas = CaixaDay.objects.filter(num_reserva=num_reserva)
    hora = timezone.now().time()
    hora_atual = diminuir_horas(hora, 3)
    context_list = []

    for caixa in caixas:
        reserva = caixa.num_reserva
        if reserva.pacote:
            pacote = reserva.pacote.id
        pet = caixa.pet
        desc = caixa.desconto
        servicos_adicionais = caixa.num_reserva.servicos_adicionais

        if servicos_adicionais is not None and servicos_adicionais.valor_servico is not None:
            serv = servicos_adicionais.valor_servico
        else:
            serv = 0
        try:
            pacotes = PacoteCliente.objects.get(pacote_id=pacote)
            quant = pacotes.quantidade_dias
            preco = pacotes.pacote.quantidade_dias
        
            if quant == preco:
                val = reserva.pacote.preco
                desc = (desc/100) * val
                numero = (val - desc) + serv
                total = format(numero, '.2f')
                caixa.total = total
            elif quant != preco:
                val = reserva.pacote.preco
                total = val
                caixa.total = total
            else:
                desc = (desc/100) * 60
                numero = (60 - desc) + serv
                total = format(numero, '.2f')
                caixa.total = total
            caixa.save()
        except:
            if reserva.pacote:
                total = 0
                caixa.total = total
            else:
                desc = (desc/100) * 60
                numero = (60 - desc) + serv
                total = format(numero, '.2f')
                caixa.total = total 
            caixa.save()

    context = {
        'total': total,
        'hora_atual': hora_atual,
        'reserva': reserva,
        'num_reserva': reserva.num_reserva,
        'nome_pet': pet.nome,
        'nome_tutor': pet.nome_tutor,
        'cpf_tutor': pet.cpf_tutor,
        'data': reserva.data,
        'hora_entrada': reserva.hora_entrada,
        'usuario': reserva.usuario,
        'relatorio': caixa.relatorio_estadia,
        'desconto': caixa.desconto,
        'servicos': servicos_adicionais,
        'metodo': caixa.metodo_de_pagamento,
    }

    context_list.append(context)

    template_path = 'relatorio_reservaday.html'
    template = get_template(template_path)
    html = template.render({'context_list': context_list})

    buffer = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), buffer)

    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'filename="relatorio_reservasday.pdf"'
    return response
@login_required(login_url="/auth/login/")
def relatorio_reservasbanho(request, num_reserva):
    # Get the Caixa objects for the given num_reserva
    caixas = CaixaBanho.objects.filter(num_reserva=num_reserva)
    hora = timezone.now().time()
    hora_atual = diminuir_horas(hora, 3)

    
    # Create a list to hold the data for each Caixa object
    context_list = []

    # Loop through the queryset and create a dictionary for each Caixa object
    for caixa in caixas:
        # Get the Reserva and Pet objects associated with the Caixa object
        reserva = caixa.num_reserva
        pet = caixa.pet
        desc = caixa.desconto
        val = caixa.num_reserva.tipo_banho.valor_servico
    
    desc = (desc/100)*val
    numero = (val-desc)
    total = format(numero, '.2f')
    caixa.total = total
    caixa.save()

        # Create a dictionary to hold the data for the PDF
    context = {
        'total': total,
        'hora_atual':hora_atual,
        'reserva': reserva,
        'num_reserva': reserva.num_reserva,
        'nome_pet': pet.nome,
        'nome_tutor': pet.nome_tutor,
        'cpf_tutor': pet.cpf_tutor,
        'data': reserva.data_reserva,
        'hora': reserva.hora_reserva,
        'usuario': reserva.banhista,
        'relatorio':caixa.relatorio_estadia,
        'desconto':caixa.desconto,
        'servicos':reserva.tipo_banho,
        'metodo':caixa.metodo_de_pagamento,

        
    }

    context_list.append(context)

    # Render the PDF template with the context data
    template_path = 'relatorio_reservabanho.html'
    template = get_template(template_path)
    html = template.render({'context_list': context_list})

    # Create a BytesIO buffer to receive the PDF output
    buffer = io.BytesIO()

    # Generate the PDF output using the BytesIO buffer
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), buffer)

    # Return the PDF as an HTTP response
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'filename="relatorio_reservas.pdf"'
    return response

def calcular_total(num_reserva):
    caixa = Caixa.objects.get(num_reserva=num_reserva)
    data_entrada = caixa.num_reserva.data_entrada
    data_saida = caixa.num_reserva.data_saida
    
    peso = caixa.pet.peso
    if peso <= 9:
        porte = "P"
    if peso >= 10 and peso <25:
        porte = "M"
    if peso >= 25:
        porte = "G"    
        
    duracao = (data_saida - data_entrada).days
    
    if duracao <= 4 and porte == "P":
        taxa = 75
    if duracao <= 4 and porte == "M":
        taxa = 85
    if duracao <= 4 and porte == "G":
        taxa = 95
    if duracao > 4 and duracao <= 9 and porte == "P":
        taxa = 70
    if duracao > 4 and duracao <= 9 and porte == "M":
        taxa = 80
    if duracao > 4 and duracao <= 9 and porte == "G":
        taxa = 90  
    if duracao > 9 and duracao <= 14 and porte == "P":
        taxa = 65 
    if duracao > 9 and duracao <= 14 and porte == "M":
        taxa = 75 
    if duracao > 9 and duracao <= 14 and porte == "G":
        taxa = 85 
    if duracao > 15 and duracao <= 19 and porte == "P":
        taxa = 60  
    if duracao > 15 and duracao <= 19 and porte == "M":
        taxa = 70    
    if duracao > 15 and duracao <= 19 and porte == "G":
        taxa = 80 
    if duracao > 19 and porte == "P":
        taxa = 55 
    if duracao > 19 and porte == "M":
        taxa = 65 
    if duracao > 19 and porte == "G":
        taxa = 75 
        
    total = duracao * taxa
    return total
@login_required(login_url="/auth/login/")
def ficha_reserva(request):
    if request.method == 'POST':
        nome_pet = request.POST.get('pet')
        try:
            reserva = Reserva.objects.get(pet__nome=nome_pet)
            return render(request, 'ficha_reserva.html', {'reserva': reserva})
        except Reserva.DoesNotExist:
            return render(request, 'reserva_nao_encontrada.html')
    return render(request, 'proc_reserva.html')
@login_required(login_url="/auth/login/")
def exibir_reserva(request, num_reserva):
    reserva = get_object_or_404(Reserva, num_reserva=num_reserva)
    return render(request, 'ficha_reserva.html', {'pet': reserva})
@login_required(login_url="/auth/login/")
def relatorio_caixasssss(request):
    data_atual = datetime.now().date()
    data_inicio = data_atual - timedelta(days=30)
    hora = timezone.now().time()
    hora_atual = diminuir_horas(hora, 3)
    
    # Get the CaixaDay objects for the given num_reserva
    total = Caixa.objects.filter(data__range=(data_inicio, data_atual)).aggregate(total=Sum('total'))['total']
    totalday = CaixaDay.objects.filter(data__range=(data_inicio, data_atual)).aggregate(total=Sum('total'))['total']
    
    debito = Caixa.objects.filter(metodo_de_pagamento='Cartão de Debito', data__range=(data_inicio, data_atual))
    total_debito = Caixa.objects.filter(metodo_de_pagamento='Cartão de Debito', data__range=(data_inicio, data_atual)).aggregate(total=Sum('total'))['total']
    credito = Caixa.objects.filter(metodo_de_pagamento='Cartão de Crédito', data__range=(data_inicio, data_atual))
    total_credito = Caixa.objects.filter(metodo_de_pagamento='Cartão de Crédito', data__range=(data_inicio, data_atual)).aggregate(total=Sum('total'))['total']
    
    dinheiro = Caixa.objects.filter(metodo_de_pagamento='Dinheiro', data__range=(data_inicio, data_atual))
    total_dinheiro = Caixa.objects.filter(metodo_de_pagamento='Dinheiro', data__range=(data_inicio, data_atual)).aggregate(total=Sum('total'))['total']
    
    pix = Caixa.objects.filter(metodo_de_pagamento='Pix', data__range=(data_inicio, data_atual))
    total_pix = Caixa.objects.filter(metodo_de_pagamento='Pix', data__range=(data_inicio, data_atual)).aggregate(total=Sum('total'))['total']
    
    debito_day = CaixaDay.objects.filter(metodo_de_pagamento='Cartão de Debito', data__range=(data_inicio, data_atual))
    total_debitoday = CaixaDay.objects.filter(metodo_de_pagamento='Cartão de Debito', data__range=(data_inicio, data_atual)).aggregate(total=Sum('total'))['total']
    
    credito_day = CaixaDay.objects.filter(metodo_de_pagamento='Cartão de Crédito', data__range=(data_inicio, data_atual))
    total_creditoday = CaixaDay.objects.filter(metodo_de_pagamento='Cartão de Crédito', data__range=(data_inicio, data_atual)).aggregate(total=Sum('total'))['total']
    
    dinheiro_day = CaixaDay.objects.filter(metodo_de_pagamento='Dinheiro', data__range=(data_inicio, data_atual))
    total_dinheiroday = CaixaDay.objects.filter(metodo_de_pagamento='Dinheiro', data__range=(data_inicio, data_atual)).aggregate(total=Sum('total'))['total']
    
    pix_day = CaixaDay.objects.filter(metodo_de_pagamento='Pix', data__range=(data_inicio, data_atual))
    total_pixday = CaixaDay.objects.filter(metodo_de_pagamento='Pix', data__range=(data_inicio, data_atual)).aggregate(total=Sum('total'))['total']
    

   

    # Create a list to hold the data for each CaixaDay object
    context_list = []

    # Loop through the queryset and process each CaixaDay object
        # Create a dictionary to hold the data for the PDF
    context = {
        'hora_atual': hora_atual,
        'debito':debito,
        'total_debito':total_debito,
        'total_credito':total_credito,
        'total_dinheiro':total_dinheiro,
        'total_pix':total_pix,
        'credito':credito,
        'dinheiro':dinheiro,
        'pix':pix,
        'debito_day':debito_day,
        'credito_day':credito_day,
        'dinheiro_day':dinheiro_day,
        'pix_day':pix_day,
        'total_debitoday':total_debitoday,
        'total_creditoday':total_creditoday,
        'total_dinheiroday':total_dinheiroday,
        'total_pixday':total_pixday,
        'total':total,
        'totalday':totalday,
        
        
    }

    context_list.append(context)

    # Render the PDF template with the context data
    template_path = 'relatorio_vendas.html'
    template = get_template(template_path)
    html = template.render({'context_list': context_list})

    # Create a BytesIO buffer to receive the PDF output
    buffer = io.BytesIO()

    # Generate the PDF output using the BytesIO buffer
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), buffer)

    # Return the PDF as an HTTP response
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'filename="relatorio_caixa.pdf"'
    return response