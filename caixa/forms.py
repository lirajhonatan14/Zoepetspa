from django import forms
from .models import Caixa, CaixaDay, CaixaBanho


class CaixaForm(forms.ModelForm):

    class Meta:
        model = Caixa
        fields = ['relatorio_estadia','desconto', 'metodo_de_pagamento']
        widgets = {
            #'usuario': forms.HiddenInput(),
            #'num_reserva': forms.HiddenInput(),
            'data':forms.HiddenInput(),
            
            'pet': forms.HiddenInput(),
        }
    def save(self, commit=True, usuario=None):
        reserva = super().save(commit=False)
        if usuario:
            reserva.usuario = usuario
        if commit:
            reserva.save()
        return reserva
    
class CaixaDayForm(forms.ModelForm):
    
    class Meta:
        model = CaixaDay
        fields = ['relatorio_estadia','desconto', 'metodo_de_pagamento']
        widgets = {
            #'usuario': forms.HiddenInput(),
            #'num_reserva': forms.HiddenInput(),
            'data':forms.HiddenInput(),
            'pet': forms.HiddenInput(),
        }
    def save(self, commit=True, usuario=None):
        reserva = super().save(commit=False)
        if usuario:
            reserva.usuario = usuario
        if commit:
            reserva.save()
        return reserva
    
class CaixaBanhoForm(forms.ModelForm):

    class Meta:
        model = CaixaBanho
        fields = ['relatorio_estadia','desconto', 'metodo_de_pagamento']
        widgets = {
            #'usuario': forms.HiddenInput(),
            #'num_reserva': forms.HiddenInput(),
            'data':forms.HiddenInput(),
            
            'pet': forms.HiddenInput(),
        }
    def save(self, commit=True, usuario=None):
        reserva = super().save(commit=False)
        if usuario:
            reserva.usuario = usuario
        if commit:
            reserva.save()
        return reserva
    
    

