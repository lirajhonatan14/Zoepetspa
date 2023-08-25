from django.contrib import admin
from .models import Reserva, ReservaDay,ServicosAdicionais, Pacote, PacoteCliente, ReservaBanho

admin.site.register(Reserva)
admin.site.register(ReservaDay)
admin.site.register(ServicosAdicionais)
admin.site.register(Pacote)
admin.site.register(PacoteCliente)
admin.site.register(ReservaBanho)

