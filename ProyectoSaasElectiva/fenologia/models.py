from django.db import models
from django.contrib.auth.models import User


class Cultivador(models.Model):
	user = models.OneToOneField(User)

	def __unicode__(self):
		return '%s %s' % (self.user.first_name,self.user.last_name)

class Administrador(models.Model):
	user = models.OneToOneField(User)

	def __unicode__(self):
		return '%s %s' % (self.user.first_name,self.user.last_name)


class TipoCultivo(models.Model):
	nombre_tipo_cultivo = models.CharField(max_length=250)

	def __unicode__(self):
		return self.nombre_tipo_cultivo

class EstadoFenologico(models.Model):
	nombre_Estado_Fenologico = models.CharField(max_length=250)
	temperatura_estado = models.IntegerField()
	humedad_estado = models.IntegerField()
	duracion = models.IntegerField()
	tipo_cultivo = models.ForeignKey(TipoCultivo)
	def __unicode__(self):
		return self.nombre_Estado_Fenologico


class Cultivo(models.Model): 
 	nombre_cultivo = models.CharField(max_length = 250)
 	tipo_cultivo = models.ForeignKey(TipoCultivo)
 	cultivador = models.ForeignKey(Cultivador)

 	def __unicode__(self):
 		return self.nombre_cultivo


class Registro(models.Model):
	fecha_registro = models.DateField(null=False)
	tempertatura = models.FloatField()
	humedad = models.FloatField()
	cultivo = models.ForeignKey(Cultivo)
	estado_fenologico = models.ForeignKey(EstadoFenologico)

	def __unicode__(self):
		return '%s %s' % (self.tempertatura,self.humedad)

