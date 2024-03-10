from django.contrib.auth.models import User
from django.db import models
# Create your models here.

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length = 8)
    direccion = models.CharField(max_length=250, null=True, blank=True)
    ci = models.CharField(max_length=11, unique=True)
    sexo = models.CharField(max_length=1)
    email = models.CharField(max_length=150, unique=True, null=False)
    
    def __str__(self):
        return self.user.username