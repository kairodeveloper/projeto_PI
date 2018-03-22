# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.urls import reverse

# Create your views here.
from django.utils.html import strip_tags

from core.models import Noticia, Comment, Evento, Comment_evento
from core.forms import ImageUploadForm, ImageUploadFormEvento
from perfis.models import *


def esta_logado(request):
    if not request.user.is_authenticated:
        return False
    return True

def get_perfil_logado(request):
    return request.user.perfil

def home(request):

    recentes = Noticia.objects.all()
    recentes = recentes[::-1]
    recentes = recentes[0:4]

    eventos = Evento.objects.all()
    eventos = eventos[::-1]
    eventos = eventos[0:3]

    if esta_logado(request):
        perfil = get_perfil_logado(request)
        return render(request, 'core/home.html', {'perfil': perfil,'recentes':recentes,'eventos':eventos})

    return render(request, 'core/home.html',{'recentes':recentes,'eventos':eventos})


def login_view(request):
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)

    user = authenticate(username=username, password=password)
    if esta_logado(request):
        return HttpResponseRedirect(reverse('home'))
    else:
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return render(request, 'core/login.html', {'error': 'Username ou senha inválidos!'})

        else:
            return render(request, 'core/login.html')

@login_required
def logout_view(request):
    if esta_logado(request):
        logout(request)
        return HttpResponseRedirect(reverse('home'))
    return HttpResponseRedirect(reverse('home'))

@login_required
def membros(request):
    if not esta_logado(request):
        return redirect('home')
    else:
        if get_perfil_logado(request).permissao.is_admin:
            return render(request, 'core/membros.html')
        else:
            return redirect('home')

@login_required
def perfil(request):
    if not esta_logado(request):
        return redirect('home')
    else:
        perfil = get_perfil_logado(request)
        if perfil.permissao.is_admin:
            noticias = perfil.autor.all()
            return render(request, 'core/perfil_noticias.html', {'perfil': perfil, 'noticias': noticias.reverse()})
        else:
            return redirect('home')

@login_required
def add_noticia(request):

    perfil = get_perfil_logado(request)


    if not perfil.permissao.is_admin:
        return redirect('home')

    error = False
    funcao = "Adicionar notícia"


    if request.method=='POST':
        form = ImageUploadForm(request.POST, request.FILES)
        new_titulo = request.POST.get('titulo', False)
        primeiro = request.POST.get('primeiro',False)
        segundo = request.POST.get('segundo', False)
        final = request.POST.get('final', False)

        if not esta_logado(request):
            return redirect('home')
        else:

            noticia_exists = Noticia.objects.filter(titulo=new_titulo).exists()
            if noticia_exists:
                error=True
                return render(request, 'core/add_noticia.html', {'perfil': perfil, 'error':error,'funcao':funcao})
            elif form.is_valid():
                noticia = Noticia(titulo=new_titulo, autor=perfil, primeiro_paragrafo=primeiro, segundo_paragrafo=segundo, consideracao_final=final)
                noticia.capa_noticia = form.cleaned_data['image']
                noticia.save()
                return redirect('perfil')

    return render(request, 'core/add_noticia.html',  {'perfil':perfil,'error':error,'funcao':funcao})



def show_noticia(request, noticia_id):
    noticia = Noticia.objects.get(id=noticia_id)
    comments = noticia.comentarios_post.all()
    if esta_logado(request):
        perfil = get_perfil_logado(request)
        is_same = False

        if perfil.usuario==noticia.autor.usuario:
            is_same=True

        if request.method=="POST":
            comentario = request.POST.get('comment',False)
            comment = Comment(noticia=noticia, comentario=comentario,autor=perfil)
            comment.save()
            return redirect('noticia' ,noticia_id)

        return render(request, 'core/noticia.html', {'perfil': perfil,'noticia':noticia,'comments':comments,'is_same':is_same})
    else:
        return render(request, 'core/noticia.html',
                      {'noticia': noticia, 'comments': comments})

@login_required
def delete_noticia(request, noticia_id):
    if not get_perfil_logado(request).permissao.is_admin:
        return redirect('home')
    noticia = Noticia.objects.get(id=noticia_id)
    noticia.delete()
    return redirect('perfil')

@login_required
def edit_noticia(request, noticia_id):
    error = False
    funcao = "Editar notícia"
    noticia = Noticia.objects.get(id=noticia_id)

    if not perfil.permissao.is_admin:
        return redirect('home')

    if request.method=='POST':
        form = ImageUploadForm(request.POST, request.FILES)
        new_titulo = request.POST.get('titulo', False)
        primeiro = request.POST.get('primeiro',False)
        segundo = request.POST.get('segundo', False)
        final = request.POST.get('final', False)

        if not esta_logado(request):
            return redirect('home')
        else:

            if form.is_valid():
                noticia.titulo=new_titulo
                noticia.primeiro_paragrafo=primeiro
                noticia.segundo_paragrafo=segundo
                noticia.consideracao_final=final
                noticia.capa_noticia = form.cleaned_data['image']
                noticia.save()
                return redirect('perfil')


    return render(request, 'core/add_noticia.html',  {'perfil':perfil,'error':error,'funcao':funcao,'noticia':noticia})

@login_required
def perfil_eventos(request):
    if not esta_logado(request):
        return redirect('home')
    if not get_perfil_logado(request).permissao.is_admin:
        return redirect('home')
    else:
        perfil = get_perfil_logado(request)
        eventos = Evento.objects.all()
        return render(request, 'core/perfil_eventos.html', {'perfil': perfil, 'eventos':eventos})


@login_required
def add_evento(request):
    perfil = get_perfil_logado(request)

    if not perfil.permissao.is_admin:
        return redirect('home')

    error = False
    funcao = "Adicionar evento"

    if request.method=='POST':
        form = ImageUploadFormEvento(request.POST, request.FILES)
        new_titulo = request.POST.get('titulo', False)
        descricao = request.POST.get('descricao',False)
        date = request.POST.get('date', False)
        hora = request.POST.get('hour',False)
        local = request.POST.get('local', False)
        valor = request.POST.get('value', False)

        if not esta_logado(request):
            return redirect('home')
        else:

            evento_exists = Evento.objects.filter(titulo=new_titulo).exists()
            if evento_exists:
                error=True
                return render(request, 'core/add_evento.html', {'perfil': perfil, 'error':error,'funcao':funcao})
            elif form.is_valid():
                evento = Evento(titulo=new_titulo, descricao=descricao,data_evento=date,hora_evento=hora,local=local, valor=valor)
                evento.img_principal = form.cleaned_data['image']
                evento.save()
                return redirect('eventos')

    return render(request, 'core/add_evento.html', {'perfil': perfil, 'error': error, 'funcao': funcao})

@login_required
def delete_evento(request, evento_id):
    if not get_perfil_logado(request).permissao.is_admin:
        return redirect('home')
    evento = Evento.objects.get(id=evento_id)
    evento.delete()
    return redirect('eventos')

@login_required
def edit_evento(request, evento_id):
    error = False
    funcao = "Editar evento"
    evento = Evento.objects.get(id=evento_id)
    perfil = get_perfil_logado(request)

    if not perfil.permissao.is_admin:
        return redirect('home')

    if request.method == 'POST':
        form = ImageUploadFormEvento(request.POST, request.FILES)
        new_titulo = request.POST.get('titulo', False)
        descricao = request.POST.get('descricao', False)
        date = request.POST.get('date', False)
        hora = request.POST.get('hour', False)
        local = request.POST.get('local', False)
        valor = request.POST.get('value', False)

        if not esta_logado(request):
            return redirect('home')
        else:

            if form.is_valid():
                evento.titulo = new_titulo
                evento.descricao = descricao
                evento.data_evento = date
                evento.hora = hora
                evento.local = local
                evento.valor = valor
                evento.img_principal = form.cleaned_data['image']
                evento.save()
                return redirect('evento',evento_id)

    return render(request, 'core/add_evento.html', {'perfil': perfil, 'error': error, 'funcao': funcao,'evento':evento})



def show_evento(request, evento_id):
    evento = Evento.objects.get(id=evento_id)
    comments = evento.comentarios_evento.all()

    if esta_logado(request):
        perfil = get_perfil_logado(request)

        if request.method == "POST":
            comentario = request.POST.get('comment', False)
            comment = Comment_evento(evento=evento, comentario=comentario, autor=perfil)
            comment.save()
            return redirect('evento', evento_id)

        return render(request, 'core/evento.html', {'perfil': perfil, 'evento': evento, 'comments': comments})
    else:
        return render(request, 'core/evento.html', {'evento': evento, 'comments': comments})

def cadastro(request):

    if request.method=='POST':
        faixa = request.POST.get('faixa', False)
        nome = request.POST.get('nome', False)
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        telefone = request.POST.get('telefone', False)
        data_nasc = request.POST.get('data_nasc', False)
        chave = request.POST.get('chave_acesso', False)
        email = request.POST.get('email', False)

        if esta_logado(request):
            return redirect('home')
        else:
            user_exists = User.objects.filter(username=username).exists()
            email_exists = User.objects.filter(email=email).exists()

            if user_exists or email_exists:
                return render(request, 'core/cadastro.html',{'error':'Usuário já existe'})

            else:
                permissao_exists = Permissao_perfil.objects.filter(codigo=chave).exists()
                if not permissao_exists:
                    return render(request, 'core/cadastro.html', {'error': 'Chave de acesso inválida'})
                else:

                    permissao = Permissao_perfil.objects.get(codigo=chave)
                    user = User(username=username, email=email)
                    user.set_password(password)
                    user.save()
                    perfil = Perfil()
                    perfil.nome=nome
                    perfil.telefone=telefone
                    perfil.faixa=faixa
                    perfil.aniversario=data_nasc
                    perfil.permissao=permissao
                    perfil.usuario=user
                    perfil.save()
                    return redirect('login')
                return render(request, 'core/cadastro.html', {'error':'Formulário inválido'})


    return render(request, 'core/cadastro.html')


def esqueci_senha(request):

    if request.method=='POST':
        email = request.POST.get('email')

        if not is_null(email):

            user_exists = User.objects.filter(email=email).exists()

            if user_exists:
                my_send_email('n','jn',email,'Clique no link abaixo, e sera redirecionado a uma pagina para a redefinir a sua senha')
            return redirect('login')

    return render(request,'core/esqueci.html')

def redefinir_senha(request):

    if request.method=='POST':
        email = request.POST.get('email', False)
        password = request.POST.get('password', False)
        rtpass = request.POST.get('rtpassword', False)

        email_exists = User.objects.filter(email=email).exists()

        if email_exists and password==rtpass:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            return redirect('login')
        return render(request, 'core/redefinir.html',{'error':'Email inválido ou senhas não correspondem'})

    return render(request, 'core/redefinir.html',{'error':''})


def is_null(field):
    if(len(field)==0):
        return True
    return False


def my_send_email(nome, email, destino, mensagem):
    import smtplib

    remetente = 'site.centro.bdm.no.reply@gmail.com'
    senha = 'gn2ps2k1997'

    destinatario = destino
    assunto = 'Recuperacao de senha'
    link = 'localhost:8000/redefinir'

    texto = '\n'.join(['From: %s' % remetente,'To: %s' % destinatario,'Subject: %s' % assunto,'','%s' % mensagem,'%s' %link,'%s' % 'Copie e cole o link no seu navegador'])

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(remetente,senha)
    server.sendmail(remetente, destinatario, texto)
    server.quit()
