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
	News model
"""
class News(models.Model):
	title = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published', auto_now_add=True)
	message= models.TextField()
	lat = models.FloatField()
	lon= models.FloatField()
	building = models.CharField(max_length=200)

"""
	Admin Reports  model
"""
class Report(models.Model):
	date = models.DateTimeField('date created', auto_now_add=True)
	message = models.TextField()
	faculty = models.CharField(max_length=200)
	title = models.CharField(max_length=200)
	lat = models.FloatField()
	lon= models.FloatField()

"""
	Phones locations model
"""
class Phone(models.Model):
	lugar = models.CharField(max_length=200)
	description = models.TextField()
	lat = models.FloatField()
	lon = models.FloatField()