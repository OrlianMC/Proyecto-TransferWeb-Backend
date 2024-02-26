from django.contrib.auth.models import User
from django.db import models
from apps.usuario.models import Perfil
    
class Cuenta(models.Model):
    no_cuenta = models.TextField(max_length=16, unique=True, primary_key=True)
    saldo = models.FloatField()
    limite_ATM = models.IntegerField()
    limite_POS = models.IntegerField()
    tipo_cuenta = models.TextField(max_length=3)
    propietario = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    
    def __str__(self) :
        return self.no_cuenta