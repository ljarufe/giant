# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('agentes.views',
    url(r'^informe_agente/$', 'informe_agente', name='informe_agente'),
)
