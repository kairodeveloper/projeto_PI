from django import forms

from core.models import Noticia, Evento
from perfis.models import Perfil


class ImageUploadForm(forms.Form):
    image = forms.ImageField()

    class Meta:
        model = Noticia


class ImageUploadFormEvento(forms.Form):
    image = forms.ImageField()

    class Meta:
        model = Evento

