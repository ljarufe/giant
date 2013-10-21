# -*- coding: utf-8 -*-

import django.forms as forms
from django.template.loader import render_to_string
from common.validators import validate_name
# models
from proyectos.models import Proyecto,FormaPago,Caracteristica,Financiamiento
from common.models import Ubicacion
from common.forms import StandartForm
from proyectos.widget import markitup


class select_popup(forms.Select):
    """
    Clase para añadir un control personalizado dentro del admin
    """
    def render(self,name,*args,**kwargs):
        html = super(select_popup,self).render(name,*args,**kwargs)
        popup = render_to_string("add_plus.html",{"field": name})
        return html + popup


class ProyectoForm(forms.ModelForm):
    """
    Formulario para agregar un proyecto
    """
    geo = forms.ModelChoiceField(Ubicacion.objects,widget=select_popup)

    class Meta:
        models = Proyecto
        fields = ["nombre","tipo_proyecto","tipo_construccion","descripcion",
                  "beneficios","servicios","pdf","estado","referencia",
                  "imagen","geo","mapa","numero_lotes","evento_inicio",
                  "forma_pago","principal"]

    TEXTDOC_TYPES = ('application/pdf',
                     'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                     'application/msword')

    def clean_pdf(self):
        """
        El documento debe ser de un tipo permitido, definido en TEXTDOC_TYPES
        """
        doc = self.cleaned_data['pdf']
        if doc:
            # Ya existía un archivo validado, este ya no tiene content_type
            try:
                ext = doc.content_type
            except:
                return doc
            # Subiendo un archivo nuevo, se necesita hacer la validación
            if not ext in self.TEXTDOC_TYPES:
                raise forms.ValidationError(u'Los tipos de archivos permitidos \
                                            son pdf, doc y docx')
            return doc


class RecomendarForm(StandartForm):
    """
    Formulario para recomdar un proyecto a una lista de 5 contactos
    """
    nombre = forms.CharField(validators=[validate_name],label=u"Tu nombre",required=True)
    nombre1 = forms.CharField(validators=[validate_name],
                              label=u"Nombre de contacto")
    email1 = forms.EmailField(label=u"e-mail")
    nombre2 = forms.CharField(validators=[validate_name],
                              label=u"Nombre de contacto",required=False)
    email2 = forms.EmailField(label=u"e-mail",required=False)
    nombre3 = forms.CharField(validators=[validate_name],
                              label=u"Nombre de contacto",required=False)
    email3 = forms.EmailField(label=u"e-mail",required=False)
    nombre4 = forms.CharField(validators=[validate_name],
                              label=u"Nombre de contacto",required=False)
    email4 = forms.EmailField(label=u"e-mail",required=False)
    nombre5 = forms.CharField(validators=[validate_name],
                              label=u"Nombre de contacto",required=False)
    email5 = forms.EmailField(label=u"e-mail",required=False)


class proyecto_form(forms.ModelForm):
    geo = forms.ModelChoiceField(Ubicacion.objects,widget=select_popup)
    evento_inicio = forms.CharField(widget=markitup())

    class Meta:
        models = Proyecto

class forma_pago_form(forms.ModelForm):
    descripcion = forms.CharField(widget=markitup())

    class Meta:
        model = FormaPago

class financiamiento_form(forms.ModelForm):
    descripcion = forms.CharField(widget=markitup())

    class Meta:
        model = Financiamiento

class caracteristicas_form(forms.ModelForm):
    descripcion = forms.CharField(widget=markitup())

    class Meta:
        model = Caracteristica
