# Generated by Django 4.1.13 on 2024-11-21 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EtapasEstudiantes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Fecha', models.DateField()),
                ('Estatus', models.CharField(max_length=16)),
                ('Grupo_est_id', models.CharField(max_length=50)),
            ],
        ),
    ]
