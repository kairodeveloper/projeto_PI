# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from perfis.models import Perfil
import uuid
import os


# Create your models here.

def get_image_path_noticia(instance, filename):
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4(), ext)
    return os.path.join("noticias", filename)

class Noticia(models.Model):
    titulo = models.CharField(max_length=100, null=False, unique=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name="autor")
    primeiro_paragrafo = models.CharField(max_length=1000,null=False)
    segundo_paragrafo = models.CharField(max_length=1000, null=True)
    consideracao_final = models.CharField(max_length=100, null=True)
    capa_noticia = models.ImageField(upload_to=get_image_path_noticia)

    def __str__(self):
        return self.titulo+" - "+self.data_criacao.__str__()

    def get_data(self):
        retorno = ""
        retorno += str(self.data_criacao.day)
        retorno += " do "
        retorno += str(self.data_criacao.month)
        retorno += " de "
        retorno += str(self.data_criacao.year)
        return retorno

class Comment(models.Model):
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name='comentarios_post', null=False)
    comentario = models.CharField(max_length=140, null=False)
    autor = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='comentarios', null=False)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def get_data(self):
        retorno = ""
        retorno += str(self.data_criacao.day)
        retorno += " do "
        retorno += str(self.data_criacao.month)
        retorno += " de "
        retorno += str(self.data_criacao.year)
        return retorno


class Imagens_noticia(models.Model):
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE,related_name="noticia", null=False)
    imagem = models.ImageField(null=False,upload_to=get_image_path_noticia)
    legenda = models.CharField(max_length=30, null=False)
    data_upload = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.noticia.titulo+" - "+self.legenda

def get_image_path_evento(instance, filename):
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4(), ext)
    return os.path.join("eventos", filename)

class Evento(models.Model):
    titulo = models.CharField(max_length=100, null=False)
    descricao = models.CharField(max_length=2000, null=False)
    data_evento = models.CharField(null=False, max_length=11)
    hora_evento = models.CharField(null=False, max_length=8)
    data_postagem = models.DateTimeField(auto_now_add=True, null=True)
    local = models.CharField(max_length=100,null=False)
    valor = models.CharField(max_length=20, null=False)
    img_principal = models.ImageField(null=False, upload_to=get_image_path_evento)

    def __str__(self):
        return self.titulo

    def get_hora(self):
        return self.hora_evento

    def get_postagem(self):
        retorno = ""
        retorno += str(self.data_postagem.day)
        retorno += " do "
        retorno += str(self.data_postagem.month)
        retorno += " de "
        retorno += str(self.data_postagem.year)
        return retorno


    def get_data(self):
        return self.data_evento


class Comment_evento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='comentarios_evento', null=False)
    comentario = models.CharField(max_length=140, null=False)
    autor = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='comentarios_eventos', null=False)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def get_data(self):
        retorno = ""
        retorno += str(self.data_criacao.day)
        retorno += " do "
        retorno += str(self.data_criacao.month)
        retorno += " de "
        retorno += str(self.data_criacao.year)
        return retorno

class Imagem_evento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="evento", null=False)
    imagem = models.ImageField(null=False, upload_to=get_image_path_evento)

    def __str__(self):
        return self.evento.titulo




