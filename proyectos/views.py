# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from django.db.models import Sum
from common.utils import direct_response, send_html_mail
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage, BadHeaderError
from common.utils import get_detalles_construccion, json_response
# Modelos
from proyectos.models import Proyecto, Construccion, Terreno, Caracteristica, Nivel, TresD, Modelo_casas
from common.models import Poligono, Punto
# forms
from proyectos.forms import RecomendarForm
from models import TresD


@csrf_exempt
def detalle_proyecto(request, id_proyecto):
    """
    Muestra toda la información pública para un proyecto
    """
    proyecto = get_object_or_404(Proyecto, pk = id_proyecto)
    receptores = None
    
    # Recomendar el proyecto
    if request.method == 'POST':
        form = RecomendarForm(request.POST)
        if form.is_valid():
            receptores = []
            # Archivo del proyecto
            pdf = []
            if proyecto.pdf:
                pdf.append(proyecto.pdf.path)

            for i in range(1, 5):
                if(form.cleaned_data['email' + str(i)]):
                    subject = u'%s le está recomendando un proyecto Giant' % \
                              form.cleaned_data['nombre']
                    data = (form.cleaned_data['nombre' + str(i)],
                            form.cleaned_data['nombre'],
                            proyecto.nombre)
                    # TODO: el mail de envío debe ser cambiado
                    
                    send_html_mail(subject, 'recomendar_email.html', data,
                                   'mauricio.llerena@aqpnet.com',
                                   [form.cleaned_data['email' + str(i)]], proyecto.pdf.path)
                    receptores.append(form.cleaned_data['email' + str(i)])

            form = RecomendarForm()
    else:
        form = RecomendarForm()
    
    construcciones = Construccion.objects.filter(proyecto = id_proyecto)
    caracteristicas = Caracteristica.objects.filter(proyectos = id_proyecto)
    area_total = Terreno.objects.filter(proyecto = id_proyecto).aggregate(Sum('area'))
    detalles_construccion = get_detalles_construccion(id_proyecto)
    referencias = proyecto.geo.referencias.all()
    tresd = TresD.objects.filter(proyecto = id_proyecto)
    modelo = Modelo_casas.objects.filter(proyecto = id_proyecto)
    terreno = Terreno.objects.filter(proyecto = id_proyecto)
    # Partes del terreno - poligonos
    poligonos_objeto = Poligono.objects.filter(ubicacion = proyecto.geo)
    poligonos = []
    for poligono in poligonos_objeto:
        puntos_objeto = Punto.objects.filter(poligono = poligono)
        poligonos.append(puntos_objeto)
                    
    return direct_response(request, 'proyectos/detalle_proyecto.html',
                           {'proyecto': proyecto,
                            'construcciones': construcciones,
                            'caracteristicas': caracteristicas,
                            'detalles_construccion': detalles_construccion,
                            'area_total': area_total,
                            'form': form,
                            'receptores': receptores,
                            'referencias': referencias,
                            'poligonos': poligonos,
                            'tresd':tresd,
                            'qTresD':tresd.count(),
                            'modelo':modelo,
                            'terreno':terreno,
                            'titulo': proyecto.nombre})

def get_detalles_json(request, id_proyecto):
    """
    Devuelve la estructura de datos con los detalles de construcción serializados
    en una respuesta json
    """
    detalles_construccion = get_detalles_construccion(id_proyecto)
    return json_response(detalles_construccion)
    
def get_aviz(request):
    id = ""
    if request.method == "GET":
        if 'tq' in request.GET:
            id = request.GET["tq"]
            description = {"nivel":("string", "Nivel"), "ambiente":("string", "Ambiente"), "acabado":("string", "Acabado"), "marca":("string", "Marca"), "medidas":("string", "Medidas"), "descripcion":("string", u"Descripción")}
            niveles_objeto = Nivel.objects.filter(construccion__proyecto = id).distinct()
            detalles_construccion = []
            for nivel in niveles_objeto:
                ambientes_objeto = nivel.ambientes.all()
                detalles_nivel = {'nivel': nivel.nombre,
                                  'ambiente': []}
                rowspan = 0
                for ambiente in ambientes_objeto:
                    acabados_objeto = ambiente.acabados.all()
                    detalles_ambiente = {'ambiente': ambiente.nombre,
                                         'acabado': []}
                    rowspan += len(acabados_objeto)
                    for acabado in acabados_objeto:
                        detalles_acabado = [acabado.nombre, acabado.marca, \
                                            acabado.medidas, acabado.descripcion]
                        detalles_ambiente['acabado'].append(detalles_acabado)
                    detalles_nivel['ambiente'].append(detalles_ambiente)
                detalles_nivel['rowspan'] = rowspan
                detalles_construccion.append(detalles_nivel)
            dataRPTA = {"desc":description, "dat":detalles_construccion}
            return HttpResponse(simplejson.dumps(dataRPTA),
                        mimetype = 'application/json')
            
    

def galeria_proyectos(request, estado, id_proyecto = None):
    """
    Galería de los proyectos
    """
    # Buscar el tipo de proyecto
    principal = ""
    estado_char = ""
    for est in Proyecto.ESTADO_CHOICES:
        if est[1].lower() == estado.lower():
            estado_char = est[0]
            break
            
    proyectos = Proyecto.objects.filter(estado = estado_char).order_by('principal').reverse()
    if id_proyecto:
        principal = get_object_or_404(Proyecto,
                                      estado = estado_char,
                                      id = id_proyecto)
    else:
        try:
            principal = Proyecto.objects.get(estado = estado[0], principal = 'True')
        except Proyecto.DoesNotExist:
            try:
                principal = Proyecto.objects.filter(estado = estado_char).order_by('?')[0]
            except IndexError:
                pass

    return direct_response(request, 'proyectos/galeria_proyectos.html',
                           {'proyectos': proyectos,
                            'principal': principal,
                            'tipo_proyecto': estado,
                            'titulo': u'Galería: %s' % estado})
                            

def get_proyecto_json(request, id_proyecto):
    """
    Obtener el resumen de un proyecto mediante una respuesta json
    """
    proyecto_objeto = Proyecto.objects.get(id = id_proyecto)
    proyecto = {'nombre': proyecto_objeto.nombre,
                'id': proyecto_objeto.id,
                'tipo': proyecto_objeto.tipo_proyecto.nombre,
                'descripcion': proyecto_objeto.descripcion,
                "imagen": u'%s' % proyecto_objeto.imagen.extra_thumbnails['resumen'], }

    return json_response(proyecto)
    
