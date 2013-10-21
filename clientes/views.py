    # -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from common.utils import direct_response
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage,BadHeaderError
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from common.utils import send_html_mail
# models
from clientes.models import Cliente
from proyectos.models import Proyecto
from common.models import Ubicacion,Poligono,Punto
# forms
from clientes.forms import ClienteForm,OportunidadForm


@csrf_exempt
def oportunidad_negocio(request):
    """
    Formulario para el envío de ofertas de terrenos a la empresa
    """
    if request.method == 'POST':
        form = OportunidadForm(request.POST)
        if form.is_valid():
            # Guardar la ubicacion y los poligonos de la oferta del cliente
            ubicacion = Ubicacion(nombre="cliente: " + form.cleaned_data['nombre'],
                                  latitud=form.cleaned_data['latitud'],
                                  longitud=form.cleaned_data['longitud'])
            ubicacion.save()
            for i in range(int(request.POST['num_ini_pol']),int(request.POST['num_pol'])):
                poligono = Poligono(ubicacion=ubicacion)
                poligono.save()
                for j in range(0,int(request.POST['num_pol_' + str(i)])):
                    punto = Punto(latitud=request.POST['lat_' + str(i) + '_' + str(j)],
                                  longitud=request.POST['lng_' + str(i) + '_' + str(j)],
                                  poligono=poligono)
                    punto.save()

            # Envío de un mail con una URL a la vista del terreno del cliente
            subject = 'Oportunidad de negocio'
            data = (form.cleaned_data['nombre'],
                    form.cleaned_data['telefono'],
                    form.cleaned_data['direccion'],
                    form.cleaned_data['asunto'],
                    form.cleaned_data['tipo'],
                    form.cleaned_data['metros'],
                    ubicacion.id)
            # TODO: el mail de envío y recepción deben ser cambiados
            msg = send_html_mail(subject,'oportunidad_negocio_email.html',data,
                               'mauricio.llerena@aqpnet.com',["mauri544@gmail.com"])
            return HttpResponseRedirect(reverse('inicio'))
    else:
        form = OportunidadForm()

    return direct_response(request,'clientes/oportunidad_negocio.html',
                           {'form': form,
                           'titulo': 'Oportunidad de negocio'})


@csrf_exempt
def registrar_cliente(request,id_proyecto=None):
    """
    Formulario para el registro de clientes
    """
    proyectos = Proyecto.objects.all()
    if id_proyecto:
        sel_proyecto = get_object_or_404(Proyecto,id=id_proyecto)
    else:
        sel_proyecto = None

    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST)
        #sin interes por algun proyecto en especifico
        if 'interes' in request.POST:
            if 'registrado' in request.POST:
                email = request.POST['email']
                try:
                    cliente = Cliente.objects.get(email=email)
                except Cliente.DoesNotExist:
                    return direct_response(request,'clientes/registrar_cliente.html',
                                           {'cliente_form': cliente_form,
                                            'proyectos': proyectos,
                                            'sel_proyecto': sel_proyecto,
                                            'invalid_user': True,
                                            'titulo': 'Registro de cliente'})

                # Envío de un mail con la información del proyecto que se solicitó
                try:
                    subject = 'Información de Giant'
                    content = u'Muchas gracias %s por comunicarte con nosotros, nuestros agentes se pondrán en contacto contigo.' % cliente.nombres
                    # TODO: colocar los e-mail correctos
                    msg = EmailMessage(subject,content,'mauricio.llerena@aqpnet.com',
                                       [email])
                    msg.send()
                except BadHeaderError:
                    return HttpResponse('Se encontró una cabecera de e-mail inválida')

                # Envíar un correo al administrador con el comentario
                subject = u"Cambio de preferencia de proyecto de un cliente"
                data = (cliente.nombres,
                        cliente.apellidos,
                        cliente.email,
                        cliente.telefono,
                        request.POST['comentario'],
                        )
                # TODO: colocar los e-mail correctos
                send_html_mail(subject,'informar_cliente_email.html',data,
                               'mauricio.llerena@aqpnet.com',['mauricio.llerena@aqpnet.com',])

                return HttpResponseRedirect(reverse('inicio'))
            else:
                if cliente_form.is_valid():
                    cliente = cliente_form.save(commit=False)
                    user = User.objects.create_user(cliente.email,
                                                    cliente.email,
                                                    '')
                    cliente.user = user
                    cliente.user.save()
                    cliente.save()

                    # Envío de un mail por el registro del cliente
                    try:
                        subject = 'Registro en Giant'
                        content = 'Gracias por registrarte como cliente de Giant, nos pondremos en contacto contigo para responder a tus preguntas.'
                        # TODO: colocar los e-mail correctos
                        msg = EmailMessage(subject,content,'mauricio.llerena@aqpnet.com',
                                           [cliente.email])
                        msg.send()
                    except BadHeaderError:
                        return HttpResponse('Se encontró una cabecera de e-mail inválida')

                    # Envíar un correo al administrador con el comentario
                    subject = u"Registro de cliente"
                    data = (cliente.nombres,
                            cliente.apellidos,
                            cliente.email,
                            cliente.telefono,
                            request.POST['comentario'],
                            )
                    # TODO: colocar los e-mail correctos
                    send_html_mail(subject,'informar_cliente_email.html',data,
                                   'mauricio.llerena@aqpnet.com',['mauricio.llerena@aqpnet.com.',])

                    return HttpResponseRedirect(reverse('inicio'))


        # El cliente ya estaba registrado, sólo desea información sobre un proyecto
        if 'registrado' in request.POST:
            email = request.POST['email']
            try:
                cliente = Cliente.objects.get(email=email)
            except Cliente.DoesNotExist:
                return direct_response(request,'clientes/registrar_cliente.html',
                                       {'cliente_form': cliente_form,
                                        'proyectos': proyectos,
                                        'sel_proyecto': sel_proyecto,
                                        'invalid_user': True,
                                        'titulo': 'Registro de cliente'})
            if 'proyecto' in request.POST:
                id_proyecto = request.POST['proyecto']
            else:
                pass
            if id_proyecto:
                proyecto = Proyecto.objects.get(id=id_proyecto)
                # Nuevo proyecto de interés para un cliente
                cliente.proyecto = proyecto

            cliente.save()

            # Envío de un mail con la información del proyecto que se solicitó
            try:
                subject = 'Información de Giant'
                content = 'La información del proyecto que solicitó se le envió junto a este e-mail como archivo adjunto.'
                # TODO: colocar los e-mail correctos
                msg = EmailMessage(subject,content,'mauricio.llerena@aqpnet.com',
                                   [email])
                if cliente.proyecto.pdf:
                    msg.attach_file(cliente.proyecto.pdf.path)
                else:
                    pass
                msg.send()
            except BadHeaderError:
                return HttpResponse('Se encontró una cabecera de e-mail inválida')

            # Envíar un correo al administrador con el comentario
            subject = u"Cambio de preferencia de proyecto de un cliente"
            data = (cliente.nombres,
                    cliente.apellidos,
                    cliente.email,
                    cliente.telefono,
                    request.POST['comentario'],
                    cliente.proyecto)
            # TODO: colocar los e-mail correctos
            send_html_mail(subject,'registrar_cliente_email.html',data,
                           'mauricio.llerena@aqpnet.com',['mauricio.llerena@aqpnet.com',])

            return HttpResponseRedirect(reverse('inicio'))

        if cliente_form.is_valid():

            cliente = cliente_form.save(commit=False)
            user = User.objects.create_user(cliente.email,
                                            cliente.email,
                                            '')
            cliente.user = user
            cliente.user.save()
            cliente.save()

            # Envío de un mail por el registro del cliente
            try:
                subject = 'Registro en Giant'
                content = 'Gracias por registrarte como cliente de Giant, la información del proyecto que solicitó se le envió junto a este e-mail como archivo adjunto.'
                # TODO: colocar los e-mail correctos
                msg = EmailMessage(subject,content,'mauricio.llerena@aqpnet.com',
                                   [cliente.email])
                if cliente.proyecto.pdf:
                    msg.attach_file(cliente.proyecto.pdf.path)
                else:
                    pass
                msg.send()
            except BadHeaderError:
                return HttpResponse('Se encontró una cabecera de e-mail inválida')

            # Envíar un correo al administrador con el comentario
            subject = u"Registro de cliente"
            data = (cliente.nombres,
                    cliente.apellidos,
                    cliente.email,
                    cliente.telefono,
                    request.POST['comentario'],
                    cliente.proyecto)
            # TODO: colocar los e-mail correctos
            send_html_mail(subject,'registrar_cliente_email.html',data,
                           'mauricio.llerena@aqpnet.com',['mauricio.llerena@aqpnet.com.',])

            return HttpResponseRedirect(reverse('inicio'))

    else:
        cliente_form = ClienteForm()

    return direct_response(request,'clientes/registrar_cliente.html',
                           {'cliente_form': cliente_form,
                            'proyectos': proyectos,
                            'sel_proyecto': sel_proyecto,
                            'invalid_user': False,
                            'titulo': 'Registro de cliente'})
