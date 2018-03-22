from core.views import *
from django.conf.urls import url, include


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^home$', home, name='home'),
    url(r'^login$', login_view, name='login'),
    url(r'^logout$', logout_view, name='logout'),
    url(r'^cadastro$', cadastro, name='cadastro'),
    url(r'^membros$', membros, name='membros'),
    url(r'^perfil$', perfil, name='perfil'),
    url(r'^add_noticia$', add_noticia, name='add_noticia'),
    url(r'^noticia/(?P<noticia_id>[0-9]+)$', show_noticia, name='noticia'),
    url(r'^noticia/editar/(?P<noticia_id>[0-9]+)$', edit_noticia, name='editar_noticia'),
    url(r'^noticia/deletar/(?P<noticia_id>[0-9]+)$', delete_noticia, name='delete_noticia'),
    url(r'^perfil_eventos$', perfil_eventos, name='eventos'),
    url(r'^add_evento$', add_evento, name='add_evento'),
    url(r'^evento/(?P<evento_id>[0-9]+)$', show_evento, name='evento'),
    url(r'^evento/deletar/(?P<evento_id>[0-9]+)$', delete_evento, name='delete_evento'),
    url(r'^evento/editar/(?P<evento_id>[0-9]+)$', edit_evento, name='editar_evento'),
    url(r'^esqueci$', esqueci_senha, name='esqueci'),
    url(r'^redefinir', redefinir_senha, name='redefinir'),

]
