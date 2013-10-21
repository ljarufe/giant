# -*- coding: utf-8 -*-

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.http import HttpResponse
from common.utils import direct_response
#delete me
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
# Modelos
from common.models import Ubicacion, Referencia, Poligono, Punto
# Forms
from common.forms import UbicacionForm


@csrf_exempt
@login_required
def nueva_ubicacion(request):
    """
    Vista para ingresar una nueva ubicación, poligonos de terrenos y 
    ubicaciones de referencias
    """
    if request.method == "POST":
        form = UbicacionForm(request.POST)
        if form.is_valid():
            ubicacion = form.save()
            
            # Guardando las referencias
            for i in range(1, int(request.POST['num_ref'])+1):
                if 'img'+str(i) in request.POST:
                    request.FILES['img'+str(i)] = ""
                referencia = Referencia(nombre=request.POST['nombre'+str(i)],
                                        descripcion=request.POST['des'+str(i)],
                                        icono=request.FILES['img'+str(i)],
                                        latitud=request.POST['lat'+str(i)],
                                        longitud=request.POST['lng'+str(i)])
                referencia.save()
                ubicacion.referencias.add(referencia)
            
            # Guardando los poligonos
            for i in range(int(request.POST['num_ini_pol']), int(request.POST['num_pol'])):
                poligono = Poligono(ubicacion=ubicacion)
                poligono.save()
                for j in range(0, int(request.POST['num_pol_'+str(i)])):
                    punto = Punto(latitud=request.POST['lat_'+str(i)+'_'+str(j)],
                                  longitud=request.POST['lng_'+str(i)+'_'+str(j)],
                                  poligono=poligono)
                    punto.save()

            return HttpResponse("<script type='text/javascript' language='javascript'>var indice = window.opener.document.getElementById('id_geo').length;var opcion = new Option('%s - %s,%s','%s');window.opener.document.getElementById('id_geo').options[indice] = opcion;window.opener.document.getElementById('id_geo').selectedIndex = indice;window.close();</script>" % (escape(ubicacion.nombre),escape(ubicacion.latitud),escape(ubicacion.longitud), escape(ubicacion._get_pk_val())))
    else:
        form = UbicacionForm()
        
    return direct_response(request, "admin/nueva_ubicacion.html",
                           {"form": form,
                            "title": "Nueva ubicacion"})
                            

@csrf_exempt
@login_required
def oferta_cliente(request, id_ubicacion):
    """
    Muestra la ubicación del terreno de un cliente con sus poligonos asociados
    """
    ubicacion = Ubicacion.objects.get(id=id_ubicacion)
    poligonos_objeto = Poligono.objects.filter(ubicacion=ubicacion)
    poligonos = []
    for poligono in poligonos_objeto:
        puntos_objeto = Punto.objects.filter(poligono=poligono)
        poligonos.append(puntos_objeto)
    
    return direct_response(request, "admin/oferta_cliente.html",
                           {"poligonos": poligonos,
                            "ubicacion": ubicacion,
                            "title": "Oferta del cliente"})    
