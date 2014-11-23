from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, parsers,renderers, permissions, viewsets, generics
from core.serializers import MyUserSerializer, IncidentSerializer, ReportSerializer, PhoneSerializer, ServiceSerializer
from core.models import MyUser, Incident, Report, Phone, Service

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer


class IncidentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Noticia to be viewed or edited.
    """
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

    def pre_save(self, obj):
        obj.owner = self.request.user
    
class PhoneViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Notification to be viewed or edited.
    """
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer
    
class ReportViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Report to be viewed or edited.
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Service to be viewd or edited.
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class IncidentList(generics.ListCreateAPIView):
    """
    List all incidents or create a new incident
    """
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

    def pre_save(self, obj):
        obj.owner = self.request.user

class IncidentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a incident instance.
    """
    queryset = Incident.objects.all()
    serializers_class = IncidentSerializer

    def pre_save(self, obj):
        obj.owner = self.request.user

class UserList(generics.ListAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer