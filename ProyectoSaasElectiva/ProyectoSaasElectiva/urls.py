from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ProyectoSaasElectiva.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$','fenologia.views.home',name='home'),
    url(r'^ingresar/','fenologia.views.ingresar',name='ingresar'),
    url(r'^logearse/','fenologia.views.logearse',name='logearse'),
    url(r'^preguntar/','fenologia.views.preguntar',name='preguntar'),
    url(r'^perfil_cultivador/','fenologia.views.perfil_cultivador',name='perfil_cultivador'),
    url(r'^listar_tipo/','fenologia.views.listar_tipo',name='listar_tipo'),
    url(r'^agregar_tipo/','fenologia.views.agregar_tipo',name='agregar_tipo'),
    url(r'^listar_fenologico/(?P<idtipo>\d+)/','fenologia.views.listar_fenologico',name='listar_fenologico'),
    url(r'^agregar_estado/', 'fenologia.views.agregar_estado', name='agregar_estado'),
    url(r'^formulario_cultivo/', 'fenologia.views.formulario_cultivo',name= 'formulario_cultivo'),
    url(r'^agregar_cultivo/','fenologia.views.agregar_cultivo', name= 'agregar_cultivo'),
    url(r'^detalle_cultivo/(?P<idcultivo>\d+)/' , 'fenologia.views.detalle_cultivo',name='detalle_cultivo'),
    url(r'^cargar_archivo/(?P<idcultivo>\d+)/', 'fenologia.views.cargar_archivo',name='cargar_archivo'),
    url(r'^formsingup/', 'fenologia.views.formsingup' , name= 'formsingup'),
    url(r'^registrar/', 'fenologia.views.registrar', name= 'registrar'),

    
    url(r'^primera/','fenologia.views.primeraVista',name='primeraVista'),
    url(r'^signup/','userprofiles.views.signup',name='signup'),

    # Url finalizar session
    url(r'^salir/','fenologia.views.salir', name='salir'),

)
