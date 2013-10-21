# -*- coding: utf-8 -*-

from django.db import models
from sorl.thumbnail.fields import ImageWithThumbnailsField
from common.models import Ubicacion
from django.conf import settings


class TipoProyecto(models.Model):
    """
    Tipo del proyecto
    """
    nombre = models.CharField(max_length=80)

    def __unicode__(self):
        return '%s' % self.nombre

    class Meta():
        verbose_name = u"tipo de proyecto"
        verbose_name_plural = u"tipos de proyecto"


class TipoConstruccion(models.Model):
    """
    Tipo de construccion
    """
    nombre = models.CharField(max_length=80)

    def __unicode__(self):
        return '%s' % self.nombre

    class Meta():
        verbose_name = u"tipo de construcción"
        verbose_name_plural = u"tipos de construcción"


class FormaPago(models.Model):
    """
    Forma de Pago
    """
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(help_text=u'Puede colocar código HTML')

    def __unicode__(self):
        return '%s' % self.nombre

    class Meta():
        verbose_name = u"forma de pago"
        verbose_name_plural = u"formas de pago"

class Financiamiento(models.Model):
    """
    Modo de financiamiento
    """
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(help_text=u'Puede colocar código HTML')

    def __unicode__(self):
        return '%s' % self.nombre

    class Meta():
        verbose_name = u'financiamiento'
        verbose_name_plural = u'financiamientos'

class Proyecto(models.Model):
    """
    Proyecto de construcción
    """
    nombre = models.CharField(max_length=200)
    tipo_proyecto = models.ForeignKey(TipoProyecto,
                                      verbose_name=u"Tipo de proyecto")
    tipo_construccion = models.ForeignKey(TipoConstruccion,
                                          verbose_name='tipo de construcción')
    descripcion = models.TextField(help_text=u'Puede colocar código HTML')
    beneficios = models.TextField(blank=True,null=True,
                                  help_text=u'Puede colocar código HTML')
    servicios = models.TextField(blank=True,null=True)
    ESTADO_CHOICES = (
        (u'A',u'Actual'),
        (u'F',u'Futuro'),
        (u'E',u'Ejecutado'),
    )
    estado = models.CharField(max_length=1,choices=ESTADO_CHOICES,default='F')
    referencia = models.CharField(max_length=200,blank=True,null=True)
    imagen = ImageWithThumbnailsField(
                upload_to='img/proyectos',
                thumbnail={'size': (625,420),
                           'options': ['upscale','max','crop']},
                extra_thumbnails={'galeria': {'size': (280,140),
                							  'options': ['crop','upscale']},
                                  'resumen': {'size': (250,155)},
                                  'detalle': {'size': (700,320)}
                                  },
                generate_on_save=True,
                verbose_name='Foto del proyecto'
                )
    geo = models.ForeignKey(Ubicacion,blank=True,null=True,
                            verbose_name="Google Map",
                            help_text="Ubique el proyecto en Google Maps")
    mapa = models.ImageField(upload_to='img/mapa',blank=True,null=True,
                             help_text="Suba una imágen del mapa del proyecto")
    plano = models.ImageField(upload_to='img/plano',blank=False,null=True,
                              help_text="Suba una imagen del plano del proyecto")
    leyenda = models.ImageField(upload_to='img/legend',blank=True,null=True,
                                help_text="Suba la leyenda asociada al plano del proyecto")
    pdf = models.FileField(upload_to="files/proyectos",blank=True,null=True,
                           verbose_name="Documento")
    numero_lotes = models.IntegerField()
    evento_inicio = models.TextField(verbose_name='Inicio de Obras',blank=True,null=False)
    forma_pago = models.ForeignKey(FormaPago,verbose_name=u"Forma de pago")
    financiamiento = models.ForeignKey(Financiamiento,verbose_name=u'Financiamiento')
    principal = models.BooleanField(default=True,help_text="Este campo le \
        dará prioridad a un proyecto para estar en la página de inicio")

    def __unicode__(self):
        return u'%s'.encode("utf-8") % self.nombre

    def save(self,*args,**kwargs):
        """
        Sólo un proyecto de cada tipo de estado puede ser el principal
        """
        if self.geo and self.geo.nombre == "":
            self.geo.nombre = self.nombre
            self.geo.save()

        if self.principal == True:
            proyectos = Proyecto.objects.filter(estado=self.estado)
            for proyecto in proyectos:
                proyecto.principal = False
                proyecto.save()
        return super(Proyecto,self).save(*args,**kwargs)

    def imagen_geo(self):
        if self.geo:
            return u'<img src="http://maps.google.com/staticmap?center=%s&markers=%s,blues&zoom=14&size=300x300&key=%s&sensor=false"/>' % (self.geo.get_latlng(),self.geo.get_latlng() ,settings.API_GOOGLE)

    imagen_geo.short_description = "Mapa"
    imagen_geo.allow_tags = True

class TresD(models.Model):
    imagen = ImageWithThumbnailsField(
                upload_to='img/proyectos',
                thumbnail={'size': (905,420),
                           'options': ['upscale','max','crop']},
                extra_thumbnails={'galeria': {'size': (400,200),
                                              'options': ['crop','upscale']},
                                  'resumen': {'size': (250,155)},
                                  'detalle': {'size': (700,320)}
                                  },
                generate_on_save=True,
                verbose_name='Foto 3D del proyecto'
                )
    proyecto = models.ForeignKey(Proyecto)

    def __unicode__(self):
        return '%s - %s' % (self.imagen,self.proyecto)

    class Meta:
        verbose_name = 'Foto 3D'
        verbose_name_plural = 'Fotos 3D'

class Caracteristica(models.Model):
    """
    Nueva característica no contemplada dentro de los otros modelos para un
    proyecto
    """
    nombre = models.CharField(max_length=80)
    descripcion = models.TextField(null=True,blank=True,
                                   verbose_name='descripción')
    proyectos = models.ForeignKey(Proyecto)

    def __unicode__(self):
        return '%s' % self.nombre


class Manzana(models.Model):
    """
    Una manzana urbana
    """
    nombre = models.CharField(max_length=1)

    def __unicode__(self):
        return '%s' % self.nombre

    def manzana_upper(self):
        if self.nombre:
            return str(self.nombre).upper()

    manzana_upper.short_description = "Manzana"


class Acabado(models.Model):
    """
    Acabado para un ambiente
    """
    nombre = models.CharField(max_length=80)
    marca = models.CharField(max_length=45)
    medidas = models.CharField(max_length=45,null=True,blank=True)
    descripcion = models.TextField(null=True,blank=True,
                                   verbose_name='descripción')

    def __unicode__(self):
        return '%s' % self.nombre


class Ambiente(models.Model):
    """
    Ambientes de un nivel 
    """
    nombre = models.CharField(max_length=60)
    descripcion = models.TextField(null=True,blank=True,
                                   verbose_name='descripción')
    largo = models.FloatField()
    ancho = models.FloatField()
    acabados = models.ManyToManyField(Acabado)

    def __unicode__(self):
        return '%s' % self.nombre

    def lista_acabados(self):
        lista = []
        options = ""
        if self.acabados:
            lista = self.acabados.all()
            for i in lista:
                options += "<li>%s</li>" % str(i)
        return "<ul>" + options + "</ul>"
    lista_acabados.short_description = "Lista Acabados"
    lista_acabados.allow_tags = True


class Nivel(models.Model):
    """
    Nivel o planta de una construcción (terraza, sotano)
    """
    nombre = models.CharField(max_length=60)
    descripcion = models.TextField(null=True,blank=True,
                                   verbose_name='descripción')
    ambientes = models.ManyToManyField(Ambiente)

    def __unicode__(self):
        return '%s' % self.nombre

    class Meta():
        verbose_name_plural = u"niveles"

    def lista_ambientes(self):
        lista = []
        options = ""
        if self.ambientes:
            lista = self.ambientes.all()
            for i in lista:
                options += "<li>%s</li>" % str(i)
        return "<ul>" + options + "</ul>"
    lista_ambientes.short_description = "Lista Ambientes"
    lista_ambientes.allow_tags = True

class Modelo_casas(models.Model):
    nombre = models.CharField(max_length=45,blank=False,null=False)
    plano = ImageWithThumbnailsField(
                upload_to='img/modelos',
                thumbnail={'size': (905,420),
                           'options': ['upscale','max','crop']},
                extra_thumbnails={'galeria': {'size': (400,200),
                                              'options': ['crop','upscale']},
                                  'resumen': {'size': (250,155)},
                                  'detalle': {'size': (700,320)}
                                  },
                generate_on_save=True,
                verbose_name='Foto del plano del modelo de proyecto'
                )
    proyecto = models.ForeignKey(Proyecto)

    def __unicode__(self):
        return '%s - %s' % (self.nombre,self.proyecto)

    class Meta:
        verbose_name = "Modelo"
        verbose_name_plural = u"Modelo Casas"

class Construccion(models.Model):
    """
    Lote construido
    """
    manzana = models.ForeignKey(Manzana)
    lote = models.CharField(max_length=3)
    modelo = models.ForeignKey(Modelo_casas,blank=True,null=True)
    ESTADO_CHOICES = (
        (u'V',u'Vendido'),
        (u'D',u'Disponible'),
        (u'S',u'Separado'),
    )
    precio = models.FloatField(null=True,blank=True)
    estado = models.CharField(max_length=1,choices=ESTADO_CHOICES,default='D')
    area_terreno = models.FloatField(verbose_name='área de terreno')
    area_techada = models.FloatField(verbose_name='área techada')
    area_construida = models.FloatField(verbose_name='área construída')
    imagen = models.ImageField(upload_to='img/',null=True,blank=True,
                               verbose_name='imágen')
    acabados = models.FileField(upload_to='files/catalogos_acabados',null=True,
                                blank=True,verbose_name=u'catálogo de acabados')
    numero_banos = models.PositiveSmallIntegerField(null=True,blank=True,\
        verbose_name='número de baños')
    numero_habitaciones = models.PositiveSmallIntegerField(null=True,\
        blank=True,verbose_name='número de habitaciones')
    frentera = models.CharField(max_length=100,null=True,blank=True)
    accesos = models.CharField(max_length=100,null=True,blank=True)
    proyecto = models.ForeignKey(Proyecto)
    niveles = models.ManyToManyField(Nivel,null=True,blank=True)

    def __unicode__(self):
        return u'%s, %s-%s' % (self.proyecto,self.manzana,self.lote)

    class Meta:
        verbose_name_plural = u'construcciones'

    def img_admin(self):
        if self.imagen:
            return u'<a href="/media/%s" target="blank">%s</a>' % (self.imagen,self.imagen)
        else:
            return 'No tiene imagen'

    img_admin.short_description = 'Imagen'
    img_admin.allow_tags = True

    def lista_niveles(self):
        lista = []
        options = ""
        if self.niveles:
            lista = self.niveles.all()
            for i in lista:
                options += "<li>%s</li>" % str(i)
        return "<ul>" + options + "</ul>"

    lista_niveles.short_description = "Lista Niveles"
    lista_niveles.allow_tags = True

class TipoTerreno(models.Model):
    """
    Tipo de un terreno de construcción
    """
    nombre = models.CharField(max_length=20)
    imagen = models.ImageField(upload_to='img/proyectos',null=True,blank=True)
    descripcion = models.TextField(null=True,blank=True)

    def __unicode__(self):
        return '%s' % self.nombre

    class Meta():
        verbose_name = u"tipo de terreno"
        verbose_name_plural = u"tipos de terreno"


class Terreno(models.Model):
    """
    Terreno para la construccion de un proyecto
    """
    manzana = models.ForeignKey(Manzana)
    lote = models.CharField(max_length=3)
    precio = models.FloatField()
    ESTADO_CHOICES = (
        (u'V',u'Vendido'),
        (u'D',u'Disponible'),
        (u'S',u'Separado'),
    )
    estado = models.CharField(max_length=1,choices=ESTADO_CHOICES,default='D')
    area = models.FloatField(verbose_name='área')
    proyecto = models.ForeignKey(Proyecto)
    tipo_terreno = models.ForeignKey(TipoTerreno,
                                     verbose_name='tipo de terreno')

    def __unicode__(self):
        return '%s, %s-%s' % (self.proyecto,self.manzana,self.lote)


