'''
Created on 09/08/2010

@author: Mauricio
'''
import django.forms as forms
from django.template.loader import render_to_string
from common.validators import validate_name
from proyectos.widget import markitup
from empresa.models import Empresa


class empresa_form(forms.ModelForm):
    resena = forms.CharField(widget = markitup())
    
    class Meta:
        model = Empresa
