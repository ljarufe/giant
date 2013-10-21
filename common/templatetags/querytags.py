# -*- coding: utf-8 -*-

from django.core.cache import cache
from django import template
from django.db.models import Max
# models
from empresa.models import Empresa


def get_empresa_common():
    """
    Retorna el objeto empresa en forma de diccionario del cache, si esta aún
    no existe o ha caducado guarda la consulta
    """
    empresa = cache.get('cache_empresa')
    if not empresa:
        id = Empresa.objects.aggregate(Max('id'))
        try:
            empresa = Empresa.objects.get(id=id['id__max'])
            cache.set('cache_empresa', empresa)
        except Empresa.DoesNotExist:
            empresa = None
    return {'empresa': empresa}


register = template.Library()

@register.inclusion_tag('common/templatetags/cache_empresa_footer.html')
def get_empresa_footer():
    """
    Etiqueta para mostrar información de la empresa en el footer
    """
    return get_empresa_common()


@register.inclusion_tag('common/templatetags/cache_empresa_info.html')
def get_empresa_info():
    """
    Etiqueta para mostrar información de la empresa en los formularios
    """
    return get_empresa_common()
    
