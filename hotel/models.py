from django.core.exceptions import ValidationError
from django.db import models
from ficha.models import FichaDog
from django.contrib.auth.models import User



class Reserva(models.Model):
    pet = models.ForeignKey(FichaDog, on_delete=models.CASCADE)
    num_reserva = models.IntegerField(primary_key=True, editable=False)
    data_entrada = models.DateField()
    data_saida = models.DateField()
    hora_entrada = models.TimeField()
    usuario  = models.ForeignKey(User, on_delete=models.CASCADE)
    HORARIO_CHOICES = (('2x_dia', 'Duas vezes por dia'),('3x_dia', 'Três vezes por dia'),('personalizado', 'Horário personalizado'),)
    horario_alimentacao = models.CharField(max_length=20, choices=HORARIO_CHOICES)
    horario_personalizado = models.CharField(max_length=20, blank=True, null=True)
    instrucoes_medicamentos = models.CharField(max_length=100, blank=True, null=True)
    ACEITAR_CHOICES = (('Sim', 'Duas vezes por dia'),('3x_dia', 'Três vezes por dia'),('personalizado', 'Horário personalizado'),)
    autorizacao_para_cuidados_medicos = models.BooleanField(default=False, choices=[(False, 'Não'), (True, 'Sim')])
    servicos_adicionais = models.ForeignKey('hotel.ServicosAdicionais', blank=True,null=True, on_delete=models.CASCADE)
    pago = models.BooleanField(default=False, null=True, choices=[(False, 'Não'), (True, 'Sim')])
    
    def clean(self):
        super().clean()
        if self.horario_alimentacao == 'personalizado':
            # Validar o input do usuário para horário personalizado
            # Certifique-se de que o campo "horario_personalizado" seja preenchido
            if not self.horario_personalizado:
                raise ValidationError("Horário personalizado requerido.")
            
    class Meta:
            db_table = 'Reserva_Hotel'
            
    def __str__(self):
        return str(self.num_reserva)

            
class ReservaDay(models.Model):
    pet = models.ForeignKey(FichaDog, on_delete=models.CASCADE)
    num_reserva = models.IntegerField(primary_key=True, editable=False)
    data = models.DateField()
    hora_entrada = models.TimeField()
    usuario  = models.ForeignKey(User, on_delete=models.CASCADE)
    instrucoes_medicamentos = models.CharField(max_length=100, blank=True, null=True)
    ACEITAR_CHOICES = (('Sim', 'Duas vezes por dia'),('3x_dia', 'Três vezes por dia'),('personalizado', 'Horário personalizado'),)
    autorizacao_para_cuidados_medicos = models.BooleanField(default=True, choices=[(False, 'Não'), (True, 'Sim')])
    servicos_adicionais = models.ForeignKey('hotel.ServicosAdicionais', blank=True,null=True, on_delete=models.CASCADE)
    pacote = models.ForeignKey('hotel.Pacote', on_delete=models.SET_NULL, null=True, blank=True)
    pago = models.BooleanField(default=False, null=True, choices=[(False, 'Não'), (True, 'Sim')])
    
    def clean(self):
        super().clean()
        if self.horario_alimentacao == 'personalizado':
            # Validar o input do usuário para horário personalizado
            # Certifique-se de que o campo "horario_personalizado" seja preenchido
            if not self.horario_personalizado:
                raise ValidationError("Horário personalizado requerido.")
            
    class Meta:
            db_table = 'Reserva_Day'
            
    def __str__(self):
        return str(self.num_reserva)
class ReservaBanho(models.Model):
    num_reserva = models.IntegerField(primary_key=True, editable=False)
    data_reserva = models.DateField()
    hora_reserva = models.TimeField()
    banhista = models.ForeignKey(User, on_delete=models.CASCADE)
    cachorro = models.CharField(max_length=100)
    tipo_banho = models.ForeignKey('hotel.ServicosAdicionais', on_delete=models.CASCADE)
    status_de_pagamento = models.BooleanField(default=False, null=True, choices=[(False, 'Não Pago'), (True, 'Pago')])
    observacoes = models.TextField(max_length=100, blank=True, null=True)
    METODO_CHOICES = (('Cartão de Crédito', 'Cartão de Crédito'),('Cartão de Debito', 'Cartão de Debito'),('Dinheiro', 'Dinheiro'),('Pix', 'Pix'),)
    metodo_de_pagamento =  models.CharField(max_length=20, choices=METODO_CHOICES)
    total = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return f"Reserva de banho para {self.cachorro} em {self.data_reserva}"
class ServicosAdicionais(models.Model):
    nome_servico = models.CharField(max_length=50, primary_key=True)
    valor_servico = models.DecimalField(max_digits=6, decimal_places=2)
    class Meta:
            db_table = 'Servicos_adicionais'
            
    def __str__(self):
        return self.nome_servico      
     
class ReservaServicoAdicional(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    servico_adicional = models.ForeignKey(ServicosAdicionais, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1) 
    class Meta:
            db_table = 'Reserva_Servicos_adicionais'

 
    def __str__(self):
        return self.reserva
    
class Pacote(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    quantidade_dias = models.IntegerField()

    def __str__(self):
        return f"{self.nome} - R${self.preco}"
    
class PacoteCliente(models.Model):
    Dog = models.ForeignKey('ficha.FichaDog', on_delete=models.CASCADE)
    pacote = models.ForeignKey('hotel.Pacote', on_delete=models.CASCADE)
    quantidade_dias = models.IntegerField()
    
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.Dog} - {self.pacote}"
    
    
        