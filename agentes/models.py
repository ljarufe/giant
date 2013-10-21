# -*- coding: utf-8 -*-

from django.db import models
# models
from common.models import Usuario
from clientes.models import Cliente
from proyectos.models import Terreno, Construccion


class Agente(Usuario):
    """
    Agente inmobiliario encargado de las ventas, posee permisos.
    """
    
    def __unicode__(self):
        return '%s %s' % (self.nombres, self.apellidos)
        

class VentaAgente(models.Model):
    """
    Venta realizada por un agente
    """
    fecha = models.DateField(verbose_name='fecha de venta')
    agente = models.ForeignKey(Agente)
    cliente = models.ForeignKey(Cliente)
    
    def __unicode__(self):
        return '%s - %s' % (agente, fecha)
        
    class Meta():
        verbose_name = u"Venta de agente"
        verbose_name_plural = u"Ventas de agente"
        
        
class VentaDetalle(models.Model):
    """
    Detalle de la venta de un agente
    """
    venta = models.ForeignKey(VentaAgente)
    terreno = models.ForeignKey(Terreno)
    construccion = models.ForeignKey(Construccion, verbose_name='construcción')
    
    class Meta():
        verbose_name = u"Detalle de venta"
        verbose_name_plural = u"Detalles de venta"
    
