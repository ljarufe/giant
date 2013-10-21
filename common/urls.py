# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('common.views',
    url(r'^ayuda_poligono/$', "ayuda_poligono", name="ayuda_poligono"),
)
