from rest_framework import serializers
from core.models import User, News, Report, Phone

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','password', 'groups','email','telephone','user_permissions', 'is_staff', 'is_active','is_superuser','last_login','date_joined')

class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = News
        fields = ('title','pub_date','message','building','lat','lon')

# class NotificationSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Notification
#         fields = ('phone','email','telefono_bool','email_bool')

class ReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Report
        fields = ('message','date','faculty','title','lat','lon')

class PhoneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Phone
        fields = ('lugar','description','lat','lon')
