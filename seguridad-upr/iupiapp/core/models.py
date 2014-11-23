from django.db import models
from django.contrib.auth.models import User
# Create your models here.

"""
	Django User extended model
"""
class MyUser(models.Model):
	user = models.OneToOneField(User)
	telephone = models.CharField(max_length=10, blank=True, default='' )

"""
	Users Incidents  model
"""
class Incident(models.Model):
	owner = models.ForeignKey('auth.User', related_name='incidents')
	pub_date = models.DateTimeField('date created', auto_now_add=True)
	message = models.TextField()
	faculty = models.CharField(max_length=200)
	title = models.CharField(max_length=200)
	lat = models.FloatField()
	lon= models.FloatField()

"""
	Admin Reports model
"""
class Report(models.Model):
	pub_date = models.DateTimeField('date created', auto_now_add=True)
	message = models.TextField()
	faculty = models.CharField(max_length=200)
	title = models.CharField(max_length=200)
	lat = models.FloatField()
	lon= models.FloatField()

"""
	Phones locations model
"""
class Phone(models.Model):
	place = models.CharField(max_length=200)
	description = models.TextField()
	lat = models.FloatField()
	lon = models.FloatField()

"""
	Service model
"""
class Service(models.Model):
	name = models.CharField(max_length=200)
	telephone = models.CharField(max_length=10, blank=False, default='')

