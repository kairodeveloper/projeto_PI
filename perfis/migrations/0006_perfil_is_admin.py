# Generated by Django 2.0.3 on 2018-03-22 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfis', '0005_perfil_perfil_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
