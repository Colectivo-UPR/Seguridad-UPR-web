# -*- encoding: utf-8 -*-
# python
from datetime import datetime
from iupiapp import settings

#django
from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.validators import RegexValidator
from django.dispatch import receiver

# allauth
from allauth.account.signals import email_confirmed

# Create your models here.


"""
	Define the custom user manager class
"""
class AuthUserManager(BaseUserManager):
	def create_user(self, email,password=None):
		if not email:
			raise ValueError("User must have an email address")

		user = self.model(email=self.normalize_email(email),)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self,email,password):
		user = self.create_user(email=email, password=password)
		user.is_active = True
		user.is_staff = True
		user.is_superuser = True
		user.is_director = True
		user.is_shiftmanager = True
		user.is_official = True
		user.save(using=self._db)
		return user

"""
	New AuthUser for the app
"""
class AuthUser(AbstractBaseUser,PermissionsMixin):
	alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', message='Only alphanumeric characters are allowed.')

	### Redefine the basic fields that would be defined in User ###
	email = models.EmailField(verbose_name='email address', unique=True, max_length=255)
	username = models.CharField(verbose_name='username', max_length=30, blank=True, default="")
	first_name = models.CharField(max_length=30, null=True, blank=True)
	last_name=models.CharField(max_length=50, null=True, blank=True)
	date_joined = models.DateTimeField(auto_now_add=True)
	is_active= models.BooleanField(default=False,null=False)
	is_staff = models.BooleanField(default=False,null=False)

	# custom fields
	is_director = models.BooleanField(default=False,null=False)
	is_shift_manager = models.BooleanField(default=False,null=False)
	is_official = models.BooleanField(default=False,null=False)

	objects = AuthUserManager()
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	def get_full_name(self):
		fullname = self.first_name +" "+ self.last_name
		return fullname

	def get_short_name(self):
		return self.email

	def __unicode__(self):
		return self.email

# django allauth signal to set user active on email confirmation
@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):

    try:
    	user = AuthUser.objects.get(email=email_address.email)
    	user.is_active = True
    	user.save()
    except AuthUser.DoesNotExist:
    	pass


"""
	Users Incidents  model
"""
class Incident(models.Model):
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='incidents')
	pub_date = models.DateTimeField('date created', auto_now_add=True)
	incident_date = models.DateTimeField('incident date', blank=False, default=datetime.now)
	message = models.TextField()
	faculty = models.CharField(max_length=200)
	title = models.CharField(max_length=200)
	lat = models.FloatField(blank=True, default=18.407633)
	lon= models.FloatField(blank=True, default=66.044355)

"""
	Admin Reports model
"""
class Report(models.Model):
	pub_date = models.DateTimeField('date created', auto_now_add=True)
	message = models.TextField()
	faculty = models.CharField(max_length=200)
	title = models.CharField(max_length=200)
	lat = models.FloatField(blank=True, default=18.407633)
	lon= models.FloatField(blank=True, default=66.044355)

"""
	Phones locations model
"""
class Phone(models.Model):
	place = models.CharField(max_length=200)
	description = models.TextField()
	lat = models.FloatField(blank=True, default=18.407633)
	lon= models.FloatField(blank=True, default=66.044355)

"""
	Service model
"""
class Service(models.Model):
	name = models.CharField(max_length=200)
	telephone = models.CharField(max_length=20, blank=False, default='')

"""
	Alert model
"""
class Alert(models.Model):
	pub_date = models.DateTimeField('date created', auto_now_add=True)
	incident_date = models.DateTimeField('incident date', blank=False)
	message = models.TextField()
	faculty = models.CharField(max_length=200)
	title = models.CharField(max_length=200)
	lat = models.FloatField(blank=True, default=18.407633)
	lon= models.FloatField(blank=True, default=66.044355)

"""
	Security Oficials
"""
class OfficialsPhones(models.Model):
	official = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='phone', null=True)
	phone_number = models.CharField(max_length=10, blank=False, default='')


"""
	Sancion_arresto
"""

class SancionArresto(models.Model):
	
# 	VPD 	= '0' # Violacion a la Politica Uso de Drogas
# 	VPA 	= '1' # Violacion a la Politica Uso de Alcohol
# 	OTROS 	= '2' # Otros

# 	SANCION_ARRESTO_TYPE_CHOICES = (
# 		)

	tipo = models.CharField(max_length=255,blank=False)

"""
	Tipo_Incidente
"""

class TipoIncidente(models.Model):

# 	ASEHOM 		= '0' # Asesinato/Homicidio
# 	HOMN 		= '1' # Homicidio negligente
# 	AGRS 		= '2' # Agresión sexual (forzada)
# 	AGRSNF		= '3' # Agresión sexual (no forzada)
# 	AGR 		= '4' # Agresión
# 	AGRA 		= '5' # Agresión agravada
# 	AME    		= '6' # Amenaza
# 	ROB 		= '7' # Robo
# 	ESC     	= '8' # Escalamiento
# 	ESCA 		= '9' # Escalamiento agravado
# 	HURVM		= '10' # Hurto vehículo de motor
# 	INC 		= '11' # Incendio
# 	APRI 		= '12' # Apropiación ilegal
# 	AMEE 		= '13' # Amenaza de Explosivos
# 	DANP 		= '14' # Daño a la propiedad
# 	ACE 		= '15' # Acecho
# 	VIOD 		= '16' # Violencia Doméstica
# 	VIOC 		= '17' # Violencia en citas
# 	OTROS 		= '18' # otros

# 	INCIDENTES_TYPE_CHOICES = (

# 			(ASEHOM, "Asesinato/Homicidio"),
# 			(HOMN, "Homicidio negligente"),
# 			(AGRS, "Agresión sexual (forzada)"),
# 			(AGRSNF, "Agresión sexual (no forzada)"),
# 			(AGR, "Agresión"),
# 			(AGRA, "Agresión agravada"),
# 			(AME, "Amenaza"),
# 			(ROB, "Robo"),
# 			(ESC, "Escalamiento"),
# 			(ESCA, "Escalamiento agravado"),
# 			(HURVM,"Hurto vehículo de motor"),
# 			(INC, "Incendio"),
# 			(APRI,"Apropiación Ilegal")
# 			(AMEE,)


# 		)
	
	tipo = models.CharField(max_length=100, blank=False)


# """
# Asesinato/Homicidio, Homicidio negligente, Agresión sexual
# (forzada), Agresión sexual (no forzada), Agresión, Agresión agravada,
# Amenaza, Robo, Escalamiento, Escalamiento agravado, Hurto vehículo de
# motor, Incendio, Apropiación ilegal, Amenaza de Explosivos, Daño a la
# propiedad, Acecho, Violencia Doméstica, Violencia en citas, otros)
# """

"""
	medio_notificacion
"""

class MedioNotificacion(models.Model):

	tipo = models.CharField(max_length=255,blank=False)

"""
	forma_se_refirio
"""

class FormaSeRefirio(models.Model):

	tipo = models.CharField(max_length=255,blank=False)

"""
	querellante
"""

class Querellante(models.Model):

	FEMENINO = '0'
	MASCULINO = '1'

	GENERO_TYPE_CHOICES = (
		(FEMENINO, 'F'),
		(MASCULINO, 'M'),
		)

	id_querella = models.IntegerField(blank=False)
	nombre = models.CharField(max_length=255,blank=False)
	direccion_residencial = models.CharField(max_length=300,blank=False)
	direccion_postal = models.CharField(max_length=300,blank=False)
	lugar_trabajo = models.CharField(max_length=300,blank=False)
	tipo_identificacion = models.CharField(max_length=255,blank=False)
	numero_identificacion = models.CharField(max_length=255,blank=False)
	tel_trabajo = models.CharField(max_length=30,blank=False)
	tel_personal = models.CharField(max_length=30,blank=False)
	sector = models.IntegerField(blank=False)
	genero = models.CharField(max_length=1, choices=GENERO_TYPE_CHOICES,default=FEMENINO)
	email = models.EmailField(verbose_name='email address', max_length=255)

"""
	Sectores
"""
class Sector(models.Model):

	tipo = models.CharField(max_length=30,blank=False)

"""
	Oficciales que Intervinieron
"""
class OficialesIntervinieron(models.Model):
	id_querella = models.IntegerField(blank=False)
	nombre = models.CharField(max_length=255,blank=False)
	turno = models.CharField(max_length=255,blank=False)
	numero_placa = models.CharField(max_length=255,blank=False)

"""
	Querellados
"""

class Querellado(models.Model):

	id_querella = models.IntegerField(blank=False)
	nombre = models.CharField(max_length=255,blank=False)
	direccion_residencial = models.CharField(max_length=300,blank=False)
	direccion_postal =  models.CharField(max_length=300,blank=False)
	telefono = models.CharField(max_length=30,blank=False)

"""
	Perjudicado
"""

class Perjudicado(models.Model):

	id_querella = models.IntegerField(blank=False)
	nombre = models.CharField(max_length=255,blank=False)
	direccion_residencial = models.CharField(max_length=300,blank=False)
	direccion_postal =  models.CharField(max_length=300,blank=False)
	telefono = models.CharField(max_length=30,blank=False)

"""
	Testigo
"""

class Testigo(models.Model):

	nombre = models.CharField(max_length=255,blank=False,default="")
	id_querella = models.IntegerField(blank=False)
	direccion_residencial = models.CharField(max_length=300,blank=False)
	direccion_postal =  models.CharField(max_length=300,blank=False)
	telefono = models.CharField(max_length=30,blank=False)

"""
	Area Geografica
"""
class AreaGeografica(models.Model):
	tipo = models.CharField(max_length=255,blank=False)

"""
	Querellas
"""

class Querella(models.Model):

	A = 'A'
	B = 'B'
	C = 'C'

	AREA_TYPE_CHOICES = (
		(A, 'A'),
		(B, 'B'),
		(C, 'C'),
		)

	numero_caso = models.CharField(max_length=255,blank=False) #a oficiales_intervinieron, a querellados, a perjudicado y a testigo. 
	fecha_informada = models.DateTimeField('fecha informada', blank=False, default=datetime.now) #(date con hora)
	medio_notificacion = models.IntegerField(blank=False)
	hay_fotos = models.BooleanField(blank=False,default=False)
	official_atendio = models.CharField(max_length=255,blank=False)
	placa_official =  models.CharField(max_length=255,blank=False)
	referido_a = models.CharField(max_length=255,blank=True)
	agente_se_notifico = models.CharField(max_length=255,blank=False)
	placa_agente = models.CharField(max_length=255,blank=False)
	numero_caso_policia = models.CharField(max_length=255,blank=False)
	forma_se_refirio = models.IntegerField(blank=False)
	accion_tomada = models.TextField(blank=False)
	fecha_incidente = models.DateTimeField('fecha incidente', blank=False, default=datetime.now)
	lugar_incidente = models.CharField(max_length=255,blank=False) 
	area_incidente = models.CharField(max_length=1, choices=AREA_TYPE_CHOICES,default=A)
	tipo_incidente = models.IntegerField(blank=False)
	crimen_odio = models.BooleanField(blank=False,default=False)
	descripcion_incidente = models.TextField(blank=False)
	sancion_arresto = models.IntegerField(blank=False)
	area_geografica = models.IntegerField(blank=False)

