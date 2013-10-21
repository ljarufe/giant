# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django import forms
from validators import validate_name,validate_phone,validate_ruc,\
                       validate_user


class Usuario(models.Model):
    """
    Usuario abstracto con todos los permisos
    """
    user = models.ForeignKey(User,unique=True)
    nombres = models.CharField(max_length=90,validators=[validate_name])
    apellidos = models.CharField(max_length=135,validators=[validate_name])
    direccion = models.CharField(max_length=90,verbose_name='dirección',
                                 null=True,blank=True)
    telefono = models.CharField(max_length=45,verbose_name='teléfono fijo',
                                null=True,blank=True,
                                validators=[validate_phone])
    celular = models.CharField(max_length=45,
                               validators=[validate_phone])
    dni = models.CharField(max_length=8,verbose_name='DNI',null=True,
                           blank=True)
    ruc = models.CharField(max_length=11,verbose_name='RUC',null=True,
                           blank=True,validators=[validate_ruc])
    ciudad = models.CharField(max_length=45,null=True,blank=True,
                              validators=[validate_name])
    email = models.EmailField(verbose_name='e-mail',validators=[validate_user])

    class Meta:
        abstract = True


class Referencia(models.Model):
    """
    Ubicación de referencia a algún proyecto
    """
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(verbose_name=u"Descripción")
    icono = models.ImageField(upload_to="img/iconos")
    latitud = models.CharField(max_length=20)
    longitud = models.CharField(max_length=20)

    def __unicode__(self):
        return '%s' % self.nombre


class Ubicacion(models.Model):
    """
    Coordenadas para representar la ubicación con google maps
    """
    nombre = models.CharField(max_length=50,null=True,blank=True)
    latitud = models.CharField(max_length=20)
    longitud = models.CharField(max_length=20)
    referencias = models.ManyToManyField(Referencia,null=True,blank=True)

    class Meta:
        verbose_name = u"Ubicación"
        verbose_name_plural = u"Ubicaciones"

    def __unicode__(self):
        return u'%s - %s, %s' % (self.nombre,self.latitud,self.longitud)

    def get_latlng(self):
        return u"%s,%s" % (self.latitud,self.longitud)


class Poligono(models.Model):
    """
    Poligono que representa un terreno, ya sea de un proyecto o la oferta de un
    cliente
    """
    ubicacion = models.ForeignKey(Ubicacion)

    def __unicode__(self):
        return u"%s" % self.ubicacion

    class Meta:
        verbose_name = u"Terreno en el mapa"
        verbose_name_plural = u"Terrenos en el mapa"


class Punto(models.Model):
    """
    Vértice de un polígono
    """
    poligono = models.ForeignKey(Poligono)
    latitud = models.CharField(max_length=20)
    longitud = models.CharField(max_length=20)

    def __unicode__(self):
        return u"%s" % self.poligono
