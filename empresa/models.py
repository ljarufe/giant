# -*- coding: utf-8 -*-

from django.db import models
from django.core.cache import cache
from django.db.models import Max

class Empresa(models.Model):
    """
    Datos dinámicos para Giant
    """
    nombre = models.CharField(max_length = 90)
    resena = models.TextField(help_text = u'Puede colocar código HTML')
    razon_social = models.CharField(max_length = 90, null = True, blank = True,
                                    verbose_name = 'razón social')
    direccion = models.CharField(max_length = 90, null = True, blank = True,
                                 verbose_name = 'direccion')
    telefono = models.CharField(max_length = 15, null = True, blank = True,
                                verbose_name = 'teléfono')
    #celular = models.CharField(max_length = 15, null = True, blank = True,
    #                            verbose_name = 'celular de contacto')
    web = models.URLField(verify_exists = False, null = True, blank = True)
    email = models.EmailField(verbose_name = 'e-mail')
    ruc = models.CharField(max_length = 11, verbose_name = 'RUC')
    
    def __unicode__(self):
        return '%s' % self.nombre
    
    def save(self, *args, **kwargs):
        """
        Si se crea una nueva empresa la anterior desaparecerá
        """
        old_id = Empresa.objects.aggregate(Max('id'))
        try:
            empresa = Empresa.objects.get(id = old_id['id__max'])
            empresa.delete()
        except Empresa.DoesNotExist:
            pass
        cache.set('cache_empresa', self)
        return super(Empresa, self).save(*args, **kwargs)        
    
    
class CuentaBanco(models.Model):
    """
    Datos para la cuenta de banco
    """
    nombre_banco = models.CharField(max_length = 20,
                                    verbose_name = 'nombre del banco')
    numero_cuenta = models.CharField(max_length = 30,
                                     verbose_name = 'número de cuenta')
    moneda = models.CharField(max_length = 20)
    empresa = models.ForeignKey(Empresa)
    
    def __unicode__(self):
        return '%s: %s' % (self.nombre_banco, self.numero_cuenta)
    
    class Meta():
        verbose_name = u"Cuenta de banco"
        verbose_name_plural = u"Cuentas de banco"
