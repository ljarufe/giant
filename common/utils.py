# -*- coding: utf-8 -*-

import codecs
from django.conf import settings
from django.core.mail import EmailMessage, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
# models
from proyectos.models import Nivel


def direct_response(request, *args, **kwargs):
    """
    Forma resumida de render to response, enviando context_instance al template
    """
    kwargs['context_instance'] = RequestContext(request)
    return render_to_response(*args, **kwargs)


def json_response(data):
    """
    Devuelve una respuesta json con la información de data
    """
    return HttpResponse(simplejson.dumps(data), mimetype = 'application/json')


def send_html_mail(subject, html_file, data, from_email, to_emails, files = None):
    """
    Envía un e-mail con contenido html el cual es extraído de un archivo de 
    codificación utf-8 ubicado en /media colocando la data correcta, la cúal 
    debe ser una lista, como parámetro opcional se pueden poner archivos
    adjuntos en forma de lista
    """
    
    content = ""
    try:
        print "hi"
        html = codecs.open('%shtml/%s' % (settings.MEDIA_ROOT, html_file), "r",
                           "utf-8")
        content = html.read() % data
        html.close()
    except:
        print "no se pudo"
    try:
        msg = EmailMessage(subject, content, from_email, to_emails)
        msg.content_subtype = "html"
        if files == None:
            pass
        else:    
            #for afile in files:
            msg.attach_file(files)
                
        msg.send()
    except BadHeaderError:
        return HttpResponse('Se encontró una cabecera de e-mail inválida')
        
        
def get_detalles_construccion(id_proyecto):
    """
    Crea una estructura de datos para almacenar los detalles en la relación de
    tablas: nivel/ambiente/acabados, la estructura de datos es de la forma:\n\n
    [{'nivel'  : 'Primer piso', 
      'rowspan': 14, 
      'ambientes': [{'acabados': [['Parket', 'XXX', '12x23m', 'parket'], 
                                  ['nombre', 'marca', 'medidas', 'descripcion'],
                     'ambiente': 'Sala'}]}]
    """
    niveles_objeto = Nivel.objects.filter(construccion__proyecto = id_proyecto).distinct()
    detalles_construccion = []
    for nivel in niveles_objeto:
        ambientes_objeto = nivel.ambientes.all()
        detalles_nivel = {'nivel': nivel.nombre,
                          'ambientes': []}
        rowspan = 0
        for ambiente in ambientes_objeto:
            acabados_objeto = ambiente.acabados.all()
            detalles_ambiente = {'ambiente': ambiente.nombre,
                                 'acabados': []}
            rowspan += len(acabados_objeto)
            for acabado in acabados_objeto:
                detalles_acabado = [acabado.nombre, acabado.marca, \
                                    acabado.medidas, acabado.descripcion]
                detalles_ambiente['acabados'].append(detalles_acabado)
            detalles_nivel['ambientes'].append(detalles_ambiente)
        detalles_nivel['rowspan'] = rowspan
        detalles_construccion.append(detalles_nivel)
    
    return detalles_construccion

