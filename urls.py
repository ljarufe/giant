# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.contrib import admin
from common.views import inicio

admin.autodiscover()

from os.path import dirname
basedir = dirname(__file__)

media = '%s/media/' % basedir

urlpatterns = patterns('',
    # aplicaciones
    (r'^agentes/', include('agentes.urls')),
    (r'^clientes/', include('clientes.urls')),
    (r'^proyectos/', include('proyectos.urls')),
    (r'^common/', include('common.urls')),
    # pagina de inicio
    url(r'^$', 'common.views.inicio', name = 'inicio'),
    url(r'giant/', 'common.views.giant_es', name = 'giant_es'),
    #url(r'^ini$', 'common.views.nuevo_inicio', name = 'nuevo_inicio'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    
    # admin
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/app/', include('admin.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # media url
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': media, 'show_indexes': True}),

    #favicon
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/media/img/recursos/iconos/favicon.ico'}),
)
