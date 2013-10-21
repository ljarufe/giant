# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('proyectos.views',
    url(r'^detalle_proyecto/(?P<id_proyecto>\d+)/$', 'detalle_proyecto', 
        name='detalle_proyecto'),
    url(r'^galeria_proyectos/(?P<estado>[\w]+)/(?P<id_proyecto>[\d]+)/$', 
        'galeria_proyectos', name='galeria_proyectos'),
    url(r'^galeria_proyectos/(?P<estado>[\w]+)/$', 'galeria_proyectos', 
        name='galeria_proyectos'),
    # respuestas json
    url(r'^get_proyecto_json/(?P<id_proyecto>\d+)/$', 'get_proyecto_json', 
        name='get_proyecto_json'),
    url(r'^get_detalles_json/(?P<id_proyecto>\d+)/$', 'get_detalles_json', 
        name='get_detalles_json'),
    url(r'^get_aviz$', 'get_aviz', 
        name='get_aviz'),
)
