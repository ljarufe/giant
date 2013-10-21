# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('clientes.views',
    url(r'^oportunidad_negocio/$', 'oportunidad_negocio', 
        name='oportunidad_negocio'),
    url(r'^registrar_cliente/(?P<id_proyecto>\d+)/$', 'registrar_cliente',
        name='registrar_cliente'),
    url(r'^registrar_cliente/$', 'registrar_cliente', 
        name='registrar_cliente'),
)
