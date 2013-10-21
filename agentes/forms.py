# -*- coding: utf-8 -*-

from django import forms
from common.forms import StandartForm
from common.validators import validate_name, validate_phone


class InformeForm(StandartForm):
    """
    Formulario para el envío de informes de agentes inmobiliarios
    """
    nombre_contacto = forms.CharField(label=u"Nombre del contacto",
                                      validators=[validate_name])
    nombre_agente = forms.CharField(label=u"Nombre de la agencia")
    telefono = forms.CharField(label=u"Teléfono", validators=[validate_phone],
                               required=False)
    email = forms.EmailField(label=u"e-mail")
    asunto = forms.CharField(widget=forms.Textarea)
    
