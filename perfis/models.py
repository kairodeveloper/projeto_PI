# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model
from enumfields import Enum, EnumField


class Faixa(Enum):
    BRANCA = 10
    AMARELA = 8
    PONTA_VERDE = 7
    VERDE = 6
    PONTA_AZUL = 5
    AZUL = 4
    PONTA_VERMELHA = 3
    VERMELHA = 2
    PONTA_PRETA = 1
    PRETA = 0



class Permissao_perfil(models.Model):

    codigo = models.CharField(max_length=5,null=False)
    is_admin = models.BooleanField(default=False)

    def gera_codigo_admin(self):
        carac = ['$',1,'g','8','*','.','b',9]
        random.shuffle(carac)
        random.shuffle(carac)
        random.shuffle(carac)
        random.shuffle(carac)
        random.shuffle(carac)

        novo = ""
        novo += str(carac[len(carac)-1])
        carac.pop()
        novo += str(carac[len(carac) - 1])
        carac.pop()
        novo += str(carac[len(carac) - 1])
        carac.pop()
        novo += str(carac[len(carac) - 1])
        carac.pop()
        novo += str(carac[len(carac) - 1])
        carac.pop()

        permissao = Permissao_perfil(codigo=novo, is_admin=True)
        return permissao

    def gera_codigo_normal(self):
        carac = ['$', 1, 'g', '8', '*', '.', 'b', 9]
        random.shuffle(carac)
        random.shuffle(carac)
        random.shuffle(carac)
        random.shuffle(carac)
        random.shuffle(carac)

        novo = ""
        novo += str(carac[len(carac) - 1])
        carac.pop()
        novo += str(carac[len(carac) - 1])
        carac.pop()
        novo += str(carac[len(carac) - 1])
        carac.pop()
        novo += str(carac[len(carac) - 1])
        carac.pop()
        novo += str(carac[len(carac) - 1])
        carac.pop()

        permissao = Permissao_perfil(codigo=novo, is_admin=False)
        return permissao


    def __str__(self):
        return self.codigo+"-"+str(self.is_admin)



class Perfil(models.Model):
    nome = models.CharField(max_length=80, null=False)
    telefone = models.CharField(max_length=11, null=False)
    faixa = EnumField(Faixa, default=Faixa.BRANCA)
    data_criacao = models.DateTimeField(auto_now_add=True)
    aniversario = models.DateField(null=False)
    usuario = models.OneToOneField(User, related_name="perfil", on_delete=models.CASCADE)
    permissao = models.ForeignKey(Permissao_perfil, on_delete=models.CASCADE, related_name="usuarios")

    @property
    def email(self):
        return self.usuario.email

    def criar_perfil(self,nome,telefone,faixa,aniversario,usuario):
        self.nome=nome
        self.telefone=telefone
        self.faixa=faixa
        self.aniversario=aniversario
        self.usuario=usuario
        self.save()

    def __str__(self):
        return self.nome

