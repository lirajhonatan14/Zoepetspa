from django.db import models

class Evento(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, null=True, blank=True)
    inicio = models.DateTimeField(null = True, blank = True)
    fim = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = "tbeventos"