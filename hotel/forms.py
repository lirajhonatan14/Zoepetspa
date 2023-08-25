from django import forms
from .models import ReservaDay, Reserva, ServicosAdicionais, ReservaBanho

class Reservaform(forms.ModelForm):
    data_entrada = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'DD/MM/AAAA'}))
    class Meta:
        model = Reserva
        fields = ['pet','data_entrada','data_saida','hora_entrada','horario_alimentacao', 'horario_personalizado','instrucoes_medicamentos', 'autorizacao_para_cuidados_medicos', 'servicos_adicionais']
        widgets = {
            'usuario': forms.HiddenInput(),
            'num_reserva': forms.HiddenInput(),
            #'servicos_adicionais': forms.CheckboxSelectMultiple()
            
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['servicos_adicionais'].queryset = ServicosAdicionais.objects.all()
        self.fields['pet'].queryset = self.fields['pet'].queryset.order_by('nome')
    def save(self, commit=True):
        reserva = super().save(commit=False)
        if commit:
            reserva.save()
        self.save_m2m()
        return reserva
    
class ReservaDayForm(forms.ModelForm):
    class Meta:
        model = ReservaDay
        fields = ['pet','data','hora_entrada','horario_alimentacao', 'horario_personalizado','instrucoes_medicamentos', 'autorizacao_para_cuidados_medicos', 'servicos_adicionais', 'pacote']
        widgets = {
            'usuario': forms.HiddenInput(),
            'num_reserva': forms.HiddenInput(),
            #'servicos_adicionais': forms.CheckboxSelectMultiple()
            'pago':forms.HiddenInput(),
            
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['servicos_adicionais'].queryset = ServicosAdicionais.objects.all()
        self.fields['pet'].queryset = self.fields['pet'].queryset.order_by('nome')
    def save(self, commit=True):
        reserva = super().save(commit=False)
        if commit:
            reserva.save()
        self.save_m2m()
        return reserva
    
class ReservaBanhoForm(forms.ModelForm):
    class Meta:
        model = ReservaBanho
        fields = ['data_reserva','hora_reserva','cachorro','tipo_banho','banhista', 'status_de_pagamento', 'observacoes']
        widgets = {
        }
    def save(self, commit=True):
        reserva = super().save(commit=False)
        if commit:
            reserva.save()
        self.save_m2m()
        return reserva
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cachorro'].queryset = self.fields['cachorro'].queryset.order_by('nome')
    
    



    