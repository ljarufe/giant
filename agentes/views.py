# -*- coding: utf-8 -*-

from common.utils import direct_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
from common.utils import send_html_mail
# forms
from forms import InformeForm
# models
from empresa.models import Empresa


@csrf_exempt
def informe_agente(request):
    """
    Formulario que un agente llena para envíar un mail al administrador del
    sitio informando de la separación de lotes
    """
    if request.method == 'POST':
        form = InformeForm(request.POST)
        if form.is_valid():
            #Envío del e-mail
            subject = 'Agente Inmobiliario: ' + \
                       form.cleaned_data['nombre_agente']
            data = (form.cleaned_data['nombre_agente'],
                    form.cleaned_data['nombre_contacto'],
                    form.cleaned_data['telefono'],
                    form.cleaned_data['email'],
                    form.cleaned_data['asunto'])                    
            # TODO: el mail de envío y recepción deben ser cambiados
            send_html_mail(subject, 'informe_agente_email.html', data, 
                           'mauricio.llerena@aqpnet.com', ['mauri544@hotmail.com'])
            return HttpResponseRedirect(reverse('inicio'))
    else:
        form = InformeForm()
        
    return direct_response(request, 'agentes/informe_agente.html',
                           {'form': form,
                           'titulo': 'Formulario Agente'})                              
