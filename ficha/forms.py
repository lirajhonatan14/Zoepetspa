from django import forms
from .models import FichaDog, Vacina, VacinaAnimal

class DogForm(forms.ModelForm):
    class Meta:
        model = FichaDog
        fields = ['nome', 'raca','data_de_nascimento','sexo', 'peso', 'tipo_alimentacao', 'restricoes_alimentares','nome_tutor','contato_tutor','cpf_tutor','endereco','veterinario', 'observacoes']
        widgets = {
            'data': forms.HiddenInput(),
        }
        

class VacinaForm(forms.ModelForm):
    class Meta:
        model = Vacina
        fields = ['nome', 'validade','nova_dose']
        widgets = {
        }
class VacinaAnimalForm(forms.ModelForm):
    class Meta:
        model = VacinaAnimal
        fields = ['pet', 'vacina','data_administracao']
        widgets = {
        }