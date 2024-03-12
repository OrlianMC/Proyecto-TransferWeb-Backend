from datetime import timezone
from django.db import models
from apps.cuenta.models import Cuenta

class Operacion(models.Model):
    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    informacion = models.CharField(max_length=100, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    servicio = models.CharField(max_length=100)
    operacion = models.CharField(max_length=100)
    monto = models.FloatField()
    moneda = models.CharField(max_length=10)

    def __str__(self):
        return self.cuenta.no_cuenta