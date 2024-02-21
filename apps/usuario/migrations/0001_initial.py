# Generated by Django 5.0.1 on 2024-02-21 05:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('telefono', models.CharField(max_length=8)),
                ('direccion', models.CharField(blank=True, max_length=250, null=True)),
                ('ci', models.CharField(max_length=11, primary_key=True, serialize=False)),
                ('sexo', models.CharField(max_length=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
