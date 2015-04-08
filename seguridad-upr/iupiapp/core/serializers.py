from rest_framework import serializers
from core.models import Incident, Report, Phone, Service, Alert, AuthUser, OfficialsPhones

class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ('id', 'email','first_name','last_name','password')
        write_only_fields = ('password',)
    def create(self, validated_data):
        user = AuthUser.objects.create_user(email= validated_data['email'], password=validated_data['password'])
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        return user

class AuthUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ('username','email','first_name','last_name')


class IncidentSerializer(serializers.ModelSerializer):

    owner = serializers.Field(source='owner.id')

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

class OfficialsPhonesSerializer(serializers.ModelSerializer):

    official = serializers.PrimaryKeyRelatedField(queryset=AuthUser.objects.all())

    class Meta:
        model = OfficialsPhones
        fields = ('id', 'official', 'phone_number')