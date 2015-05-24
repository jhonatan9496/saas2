import json
from django.template import RequestContext
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from models import *
from django.core import serializers
from django.core.files import File
import re
import time


# Create your views here.




# vista que redirecciona al login y maneja seguridad cache

def home(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/preguntar')
	return HttpResponseRedirect('/ingresar')


def ingresar(request):
	return render_to_response('login.html',context_instance=RequestContext(request))

def logearse(request):
	if request.method == 'POST':
		formulario = AuthenticationForm(request.POST)
		if formulario.is_valid:
			usuario = request.POST['username']
			clave = request.POST['password']
			acceso = authenticate(username=usuario, password=clave)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return HttpResponseRedirect('/preguntar')
				else:
					return render_to_response('no_activo.html', context_instance=RequestContext(request))
			else:
				return HttpResponseRedirect('/ingresar')
	return render_to_response('log.html',{'formulario':formulario}, context_instance=RequestContext(request))


@login_required(login_url='/logearse')
def preguntar(request):
	usuario = request.user
	cultivador = Cultivador.objects.filter(user=usuario)
	administrador = Administrador.objects.filter(user=usuario)
	if cultivador:
		return perfil_cultivador(request)
	if administrador:
		return perfil_administrador(request)
	return HttpResponse('no hay tipo usuario')


@login_required(login_url='/logearse')
def perfil_cultivador(request):
	usuario = request.user
	cultivador = Cultivador.objects.filter(user=usuario)
	if cultivador:
		cultivos = Cultivo.objects.filter(cultivador=cultivador)
		return render_to_response('Perfil_cultivador.html',locals(), context_instance=RequestContext(request))
	return HttpResponse('no hay campesino')


@login_required(login_url='/logearse')
def perfil_administrador(request):
	usuario = request.user
	administrador = Administrador.objects.filter(user=usuario)
	cultivadores = Cultivador.objects.all()
	if administrador:
		# consultas ---
		# cultivos = Cultivo.objects.filter(cultivador=cultivador)
		return render_to_response('Perfil_administrador.html',locals(), context_instance=RequestContext(request))
	return HttpResponse('no hay campesino')

@login_required(login_url='/logearse')
def listar_tipo(request):
	tipos = TipoCultivo.objects.all()
	return render_to_response('tipocultivo.html',locals(), context_instance=RequestContext(request))


@login_required(login_url='/logearse')
def agregar_tipo(request):
	if request.method == 'POST':
		tipo_cultivo = TipoCultivo(nombre_tipo_cultivo=request.POST['titulo_tipo'])
		tipo_cultivo.save()
		return HttpResponseRedirect('/listar_tipo')
	return HttpResponse('no guardo')

@login_required(login_url='/logearse')
def listar_fenologico(request,idtipo):
	tipo = TipoCultivo.objects.get(pk=idtipo)
	fenologicos = EstadoFenologico.objects.filter(tipo_cultivo=tipo)
	return render_to_response('estadofenologico.html',locals(), context_instance=RequestContext(request))

@login_required(login_url='/logearse')
def agregar_estado(request):
	if request.method == 'POST':
		cultivo = TipoCultivo.objects.get(nombre_tipo_cultivo=request.POST['tipo'])
		nombre = request.POST['nombre']
		temperatura = request.POST['temperatura']
		humedad = request.POST['humedad']
		duracion = request.POST['duracion']
		estado = EstadoFenologico(tipo_cultivo=cultivo,nombre_Estado_Fenologico=nombre,temperatura_estado=temperatura,humedad_estado=humedad,duracion=duracion)
		estado.save()
		cul = str(cultivo.id)
		link = '/listar_fenologico/'+cul+'/' 
		return HttpResponseRedirect(link)
	return HttpResponse('no guardo')

@login_required(login_url='/logearse')
def formulario_cultivo(request):
	tipocultivos = TipoCultivo.objects.all()
	return render_to_response('cultivo.html',locals(), context_instance=RequestContext(request))

@login_required(login_url='/logearse')
def agregar_cultivo(request):
	usuario = request.user
	campesino = Cultivador.objects.get(user=usuario)
	tipo = TipoCultivo.objects.get(pk=request.POST['tipo'])
	nombre = request.POST['nombre_cultivo']
	cultivo = Cultivo(nombre_cultivo=nombre,tipo_cultivo=tipo,cultivador=campesino)
	cultivo.save()
	return HttpResponseRedirect('/perfil_cultivador/')

@login_required(login_url='/logearse')
def detalle_cultivo(request,idcultivo):
	cultivo = Cultivo.objects.get(pk=idcultivo)
	registros = Registro.objects.filter(cultivo=cultivo)
	# tipo = TipoCultivo.objects.get(pk=cultivo.tipo_cultivo)
	# registro = EstadoFenologico.objects.get(tipo_cultivo=tipo)




	temperaturaEsperada=0
	# for i in registros:
	# 	temperaturaEsperada=i.estado_fenologico.temperatura_estado

	datat=[]
	j=1
	for i in registros:

		datat.append([j,  i.tempertatura, i.estado_fenologico.temperatura_estado])
		j=j+1
	j=0
	datah=[]
	j=1
	for i in registros:

		datah.append([j,  i.humedad, i.estado_fenologico.humedad_estado])
		j=j+1

	return render_to_response('grafica.html',locals(), context_instance=RequestContext(request))


	# data = [
 #        [1,  15.0, 10.0],
 #        [2,  30.9, 10.1],
 #        [3,  25.4, 10.1],
 #        [4,  11.7, 10.1],
 #        [5,  11.9, 10.1],
 #        [6,   8.8, 10.1],
 #        [7,   7.6, 10.1],
 #        [8,  12.3, 10.1],
 #        [9,  16.9, 10.1],
 #        [10, 12.8, 10.1],
 #        [11,  5.3, 10.1],
 #        [12,  6.6, 10.1],
 #        [13,  4.8, 10.1],
 #        [14,  4.2, 10.1]
 #    ]



@login_required(login_url='/logearse')
def cargar_archivo(request,idcultivo):
	if request.method == 'POST':

		cultivo = Cultivo.objects.get(pk=idcultivo)
		fenologico = EstadoFenologico.objects.get(tipo_cultivo=cultivo.tipo_cultivo)

		archivo = request.FILES['archivo']
		#archivo = codecs.open(file=archivo.file,mode='r',encoding='utf-8')
		buff = archivo.readline()
		lineas = []
		tmp = []

		i=0

		while buff:
			if i<3:
				tmp.append(buff.strip())
				i=i+1
			else :
				i=1
				lineas.append(tmp)
				tmp=[]
				tmp.append(buff.strip())

			buff = archivo.readline()

		for j in lineas:
			# separamoes en un vector y seleccionamos temperatura despues de humedad=
			dat = j[0].split(',')
			humedad = dat[3][8:]
			inthumedad = humedad.split('.')
			hu = inthumedad[0]
			h = int(hu)

			dat = j[1].split(',')
			temperatura = dat[3][12:]
			inttemp = temperatura.split('.')
			te = inttemp[0]
			t = int(te)

			nuevo_registro = Registro(fecha_registro='2015-08-15',tempertatura=int(t),humedad=int(h),cultivo=cultivo,estado_fenologico=fenologico)
			nuevo_registro.save()

			print('humedad '+ hu+' temperatura '+te)

			# agregar Registro


		url = '/detalle_cultivo/'+str(idcultivo)+'/'
	return HttpResponseRedirect(url)



@login_required(login_url='/logearse')
def salir(request):
	logout(request)
	return HttpResponseRedirect('/')


def formsingup(request):
	return render_to_response('registro.html',locals(), context_instance=RequestContext(request))

def registrar(request):
	if request.method == 'POST':
		user = User.objects.create_user(request.POST['username'],None,request.POST['password'])
		user.first_name=request.POST['first_name']
		user.last_name=request.POST['last_name']
		user.email=request.POST['email']
		user.is_active = True
		user.save()
		cultivador = Cultivador(user=user)
		cultivador.save()
	return HttpResponseRedirect('/')
		# if request.POST['tipo'] == 'estudiante' :
		# 	nuevo_estudiante = Estudiante(user=user,codigo_estudiante=request.POST['codigo_estudiantil'])
		# 	nuevo_estudiante.save()
		# 	return render_to_response('success.html',locals(), context_instance=RequestContext(request))
		# if request.POST['tipo'] == 'docente' :
		# 	areafor = Area.objects.get(pk=request.POST['area'])
		# 	nuevo_docente = Docente(user=user,area=areafor)
		# 	nuevo_docente.save()
		# 	return render_to_response('success.html',locals(), context_instance=RequestContext(request))



def primeraVista(request):
	return HttpResponse('ok')
	cultivo = Cultivo.objects.get(pk=2)
	return render(request,'primera.html' , {'cultivo':cultivo})

	# data = { 'titulo': cultivo.nombre_cultivo

	# }

	# cultivo = Cultivo.objects.all()

	# for i in cultivo:
	# 	# data['titulo']=str(i.nombre_cultivo)
	# 	data = {'titulo':str(i.nombre_cultivo)}
	# json_data= json.dumps(data)

	# data = serializers.serialize("json", Cultivo.objects.all())

	# return HttpResponse(data,content_type='application/json')







