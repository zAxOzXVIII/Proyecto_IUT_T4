# Generated by Django 4.1.13 on 2024-07-16 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_rename_is_staff_customuser_is_admin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estudiante',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
