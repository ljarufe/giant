# -*- coding: utf-8 -*-

from common.utils import direct_response
from django.db.models import Count
# Modelos
from proyectos.models import Proyecto
from empresa.models import Empresa

def old_inicio(request):
    """
    Página de inicio donde se muestran ejemplos de los 3 tipos de proyectos
    """
    # La animación inicial se debe presentar una sola vez por sesión
    if 'open_swf' in request.session:
        request.session['open_swf'] = False
    else:
        request.session['open_swf'] = True
        request.session.set_expiry(0)
    
    proyectos = Proyecto.objects.filter(estado = "A")
    empresa = Empresa.objects.get(id = 1)
        
    return direct_response(request, 'common/inicio.html',
                           {'proyectos': proyectos,
                            'empresa':empresa,
                            'mostrar_swf': request.session['open_swf'],
                            'titulo': 'Inicio'})
def giant_es(request):
    proyectos = Proyecto.objects.filter(estado = "A")
    empresa = Empresa.objects.get(id = 1)
        
    return direct_response(request, 'common/giant_es.html',
                           {'proyectos': proyectos,
                            'empresa':empresa,
                            'mostrar_swf': request.session['open_swf'],
                            'titulo': 'Giant es...'})

def inicio(request):   
    if 'open_swf' in request.session:
        request.session['open_swf'] = False
    else:
        request.session['open_swf'] = True
        request.session.set_expiry(0)
    
    proyectos = Proyecto.objects.filter(estado = "A")
    empresa = Empresa.objects.get(id = 1)
        
    return direct_response(request, 'common/index.html',
                           {'proyectos': proyectos,
                            'empresa':empresa,
                            'mostrar_swf': request.session['open_swf'],
                            'titulo': 'Inicio'})                         

def ayuda_poligono(request):
    """
    Muestra la ayuda para crear poligonos
    """
    return direct_response(request, "common/ayuda_poligono.html")

