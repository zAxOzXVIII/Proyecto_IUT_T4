# Generated by Django 4.1.13 on 2024-09-16 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_estudiante_direccion_alter_estudiante_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='estudiante',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
