# Generated by Django 2.0.3 on 2018-03-21 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_noticia_capa_noticia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticia',
            name='titulo',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]