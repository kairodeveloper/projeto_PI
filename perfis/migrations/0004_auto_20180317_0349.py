# Generated by Django 2.0.3 on 2018-03-17 03:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfis', '0003_administrador'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='administrador',
            name='usuario',
        ),
        migrations.DeleteModel(
            name='Administrador',
        ),
    ]