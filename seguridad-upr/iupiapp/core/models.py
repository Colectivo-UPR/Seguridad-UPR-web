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
		user.is_webdirector = True
		user.is_webmanager = True
		user.is_webadmin = True
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
	is_webdirector = models.BooleanField(default=False,null=False)
	is_webmanager = models.BooleanField(default=False,null=False)
	is_webadmin = models.BooleanField(default=False,null=False)

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
	telephone = models.CharField(max_length=10, blank=False, default='')

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
