from django.contrib import admin
from .models import FichaDog, Vacina, VacinaAnimal

admin.site.register(FichaDog)
admin.site.register(Vacina)
admin.site.register(VacinaAnimal)

