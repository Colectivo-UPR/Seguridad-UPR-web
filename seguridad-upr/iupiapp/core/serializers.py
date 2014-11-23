from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import Incident, Report, Phone, MyUser, Service

class MyUserSerializer(serializers.ModelSerializer):

    # get the data from the user model
    incidents = serializers.RelatedField(many=True, source='user.incidents')    
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')
    password = serializers.CharField(source='user.password') 

    class Meta:
        model = MyUser
        fields = ('username','first_name','last_name','password','email','telephone','incidents')

    # build both models from the input data
    def restore_object(self, attrs, instance=None):
        """
            Given a dictionary of deserialized field values, either update
            an existing model instance, or create a new model instance.
        """

        # if the instance is not empty assign the atributes
        if instance:
            
            instance.user.email = attrs.get('user.email', instance.user.email)
            instance.user.first_name = attrs.get('user.first_name', instance.user.first_name)
            instance.user.last_name = attrs.get('user.last_name', instance.user.last_name)
            instance.user.username = attrs.get('user.username', instance.user.username)
            instance.telephone = attrs.get('telephone', instance.telephone)
            return instance

        # no instance so create the user instance
        user = User.objects.create_user(username=attrs.get('user.username'),
                                        email=attrs.get('user.email'), 
                                        password=attrs.get('user.password'),
                                        first_name=attrs.get('user.first_name'),
                                        last_name=attrs.get('user.last_name'))

        telephone= attrs.get('telephone')

        return MyUser(user=user, telephone=telephone)

class IncidentSerializer(serializers.ModelSerializer):

    owner = serializers.Field(source='owner.username')

    class Meta:
        model = Incident
        fields = ('owner','title','pub_date','message','faculty','lat','lon')

# class NotificationSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Notification
#         fields = ('phone','email','telefono_bool','email_bool')

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('title','pub_date','message','faculty','lat','lon')

class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ('place','description','lat','lon')

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('name','telephone')