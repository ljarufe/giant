# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('admin.views',
    url(r'^nueva_ubicacion/$', "nueva_ubicacion", name="nueva_ubicacion"),
    url(r'^oferta_cliente/(?P<id_ubicacion>\d+)/$', "oferta_cliente",
        name="oferta_cliente"),
)
