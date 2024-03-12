# Generated by Django 5.0.1 on 2024-03-11 13:24

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cuenta', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(default=datetime.timezone)),
                ('servicio', models.CharField(max_length=100)),
                ('operacion', models.CharField(max_length=100)),
                ('monto', models.FloatField()),
                ('moneda', models.CharField(max_length=10)),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cuenta.cuenta')),
            ],
        ),
    ]