# -*- coding: utf-8 -*-

from common.models import Ubicacion
from django import forms


class StandartForm(forms.Form):
    """
    An standart form with error class
    """
    error_css_class = 'error'
    required_css_class = 'required'
    

class UbicacionForm(forms.ModelForm):
    """
    Formulario para la ubicación de un punto en un mapa
    """
    longitud = forms.CharField(widget=forms.HiddenInput)
    latitud = forms.CharField(widget=forms.HiddenInput)
    class Meta:
        model = Ubicacion
        fields = ["nombre", "latitud", "longitud", "referencias"]
