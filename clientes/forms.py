# -*- coding: utf-8 -*-

from django import forms
from common.validators import validate_name,validate_phone
from common.forms import StandartForm
# Modelos
from clientes.models import Cliente


class ClienteForm(forms.ModelForm):
    """
    Formulario para la clase Cliente
    """
    error_css_class = 'error'
    required_css_class = 'required'

    # Definición del formulario
    class Meta:
        model = Cliente
        fields = ('nombres','apellidos','direccion','ciudad','telefono',
                  'celular','email','interes','proyecto')


class OportunidadForm(StandartForm):
    """
    Formulario para el ingreso de una oportunidad de negocio
    """
    nombre = forms.CharField(max_length=100,validators=[validate_name])
    telefono = forms.CharField(validators=[validate_phone])
    direccion = forms.CharField(label=u'Dirección de la propiedad')
    asunto = forms.CharField(widget=forms.Textarea)
    tipo = forms.CharField(max_length=45,label='Tipo de propiedad',required=False)
    metros = forms.CharField(max_length=45,label=u'Metros cuadrados',required=False)
    longitud = forms.CharField(widget=forms.HiddenInput)
    latitud = forms.CharField(widget=forms.HiddenInput)
