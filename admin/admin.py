# -*- coding: utf-8 -*-

from django.contrib import admin
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django import http
import datetime
# Modelos
from agentes.models import *
from clientes.models import *
from empresa.models import *
from proyectos.models import *
from common.models import *
# Formularios
from proyectos.forms import ProyectoForm,proyecto_form,forma_pago_form,caracteristicas_form,financiamiento_form
from empresa.forms import empresa_form
# Generacion de csv
import csv


def exportar_csv(modeladmin,request,queryset):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + \
                                      str(datetime.date.today()) + \
                                      '.csv'
    writer = csv.writer(response)
    writer.writerow(["Nombres","Apellidos",u"Dirección".encode("utf-8"),\
                    u"Teléfono".encode("utf-8"),"Celular","Ciudad","E-mail"])

    for i in queryset:
        nombre = i.nombres
        apellidos = i.apellidos
        direccion = i.direccion
        telefono = i.telefono
        celular = i.celular
        ciudad = i.ciudad
        email = i.email
        writer.writerow([nombre.encode("utf-8"),apellidos.encode("utf-8"),\
                        direccion.encode("utf-8"),telefono,celular,\
                        ciudad.encode("utf-8"),email])
    return response

exportar_csv.short_description = "Exportar seleccionados a CSV"


class AdminProyecto(admin.ModelAdmin):
    form = proyecto_form
    list_display = ("nombre","tipo_proyecto","tipo_construccion",
                    "descripcion","estado","imagen_geo")


class AdminAmbiente(admin.ModelAdmin):
    list_display = ("nombre","descripcion","lista_acabados",)


class AdminAcabados(admin.ModelAdmin):
    list_display = ("nombre","marca","medidas","descripcion")


class AdminNiveles(admin.ModelAdmin):
    list_display = ("nombre","descripcion","lista_ambientes")


class AdminConstruccion(admin.ModelAdmin):
    list_display = ("proyecto","manzana","lote","estado","img_admin",\
                    "acabados","lista_niveles")


class AdminManzana(admin.ModelAdmin):
    list_display = ("manzana_upper",)


class AdminTerrenos(admin.ModelAdmin):
    list_display = ("manzana","lote","precio","estado","area","proyecto")


class AdminCliente(admin.ModelAdmin):
    list_display = ("apellidos","nombres","direccion","telefono","celular",
                    "ciudad","email","interes","proyecto")
    list_filter = ("ciudad","proyecto")
    actions = [exportar_csv]


class AdminReferencia(admin.ModelAdmin):
    list_display = ("nombre","descripcion","icono")


class AdminUbicacion(admin.ModelAdmin):
    list_display = ("nombre","latitud","longitud")


class AdminPoligono(admin.ModelAdmin):
    list_display = ("ubicacion",)
    list_filter = ("ubicacion",)


class AdminPunto(admin.ModelAdmin):
    list_display = ("poligono",)
    list_filter = ("poligono",)


class AdminFormaPago(admin.ModelAdmin):
    form = forma_pago_form

class AdminFinanciamiento(admin.ModelAdmin):
    form = financiamiento_form

class AdminCaracteristicas(admin.ModelAdmin):
    form = caracteristicas_form

class AdminEmpresa(admin.ModelAdmin):
    form = empresa_form

class AdminTresD(admin.ModelAdmin):
    fields = ("imagen","proyecto")
    #filter = ["proyecto", ]

class AdminModelos(admin.ModelAdmin):
    fields = ("nombre","plano","proyecto")


# agentes
admin.site.register(Agente)
# clientes
admin.site.register(Cliente,AdminCliente)
# empresas
admin.site.register(Empresa,AdminEmpresa)
admin.site.register(CuentaBanco)
# proyectos
admin.site.register(Proyecto,AdminProyecto)
admin.site.register(TipoProyecto)
admin.site.register(Construccion,AdminConstruccion)
admin.site.register(TipoConstruccion)
admin.site.register(Nivel,AdminNiveles)
admin.site.register(Ambiente,AdminAmbiente)
admin.site.register(Acabado,AdminAcabados)
admin.site.register(Terreno,AdminTerrenos)
admin.site.register(TipoTerreno)
admin.site.register(Manzana,AdminManzana)
admin.site.register(FormaPago,AdminFormaPago)
admin.site.register(Financiamiento,AdminFinanciamiento)
admin.site.register(Caracteristica,AdminCaracteristicas)
# common
admin.site.register(Ubicacion,AdminUbicacion)
admin.site.register(Referencia,AdminReferencia)
admin.site.register(Poligono,AdminPoligono)
admin.site.register(Punto,AdminPunto)
admin.site.register(Modelo_casas,AdminModelos)
admin.site.register(TresD,AdminTresD)
