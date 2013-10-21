# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.inclusion_tag('common/templatetags/display_as_ul.html')
def display_as_ul(form):
    """
    Muestra los campos del formulario en forma de lista
    """
    return {'form': form}
