from django.db import models
from apps.usuario.models import Perfil

# Create your models here.
class Servicio(models.Model):
    propietario = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    identificador = models.CharField(max_length=20)
    nombre = models.CharField(max_length=150)
    campo = models.CharField(max_length=150, blank=True)
    monto = models.FloatField()
    
    def __str__(self):
        return self.nombre