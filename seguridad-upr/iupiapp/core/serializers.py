from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import Incident, Report, Phone, Service, Alert, AuthUser

class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ('id', 'email','first_name','last_name','password')


class IncidentSerializer(serializers.ModelSerializer):

    owner = serializers.Field(source='owner.email')

    class Meta:
        model = Incident
        fields = ('id', 'owner','title','pub_date','incident_date', 'message','faculty','lat','lon')


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('id', 'title','pub_date','message','faculty','lat','lon')

class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ('id', 'place','description','lat','lon')

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'name','telephone')

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ('id', 'title','pub_date','incident_date', 'message','faculty','lat','lon')