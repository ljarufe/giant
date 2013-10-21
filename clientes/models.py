# -*- coding: utf-8 -*-

from django.db import models
# models
from common.models import Usuario
from proyectos.models import Proyecto
from django.template.defaultfilters import default

class Cliente(Usuario):
    """
    Cliente de la empresa
    """
    interes = models.BooleanField(blank = True, default = True, verbose_name = u'Información General', help_text = u'Marcar para comunicarse con nosotros, sin recibir información de un proyecto')
    proyecto = models.ForeignKey(Proyecto, blank = True, null = True)
    
    def __unicode__(self):
        return '%s %s' % (self.nombres, self.apellidos)
