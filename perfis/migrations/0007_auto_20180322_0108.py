# Generated by Django 2.0.3 on 2018-03-22 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfis', '0006_perfil_is_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permissao_perfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=5)),
                ('is_admin', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='perfil',
            name='is_admin',
        ),
    ]
