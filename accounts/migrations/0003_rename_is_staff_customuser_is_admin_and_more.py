# Generated by Django 4.1.13 on 2024-07-16 22:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_estudiante'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='is_staff',
            new_name='is_admin',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_superuser',
        ),
    ]
