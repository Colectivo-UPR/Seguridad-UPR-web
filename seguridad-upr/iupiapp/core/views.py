from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status, parsers,renderers, permissions, viewsets, generics
from core.serializers import MyUserSerializer, IncidentSerializer, ReportSerializer, PhoneSerializer, ServiceSerializer
from rest_framework.authentication import TokenAuthentication 
from core.models import MyUser, Incident, Report, Phone, Service
from core.permissions import IsOwnerOnly

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
    permission_classes = (IsOwnerOnly,)
    authentication_classes = (TokenAuthentication,)
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

    def pre_save(self, obj):
        obj.owner = self.request.user

class IncidentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a incident instance.
    """
    permission_classes = (IsOwnerOnly,)
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

class UserRegister(generics.CreateAPIView):
    """
    Register a User
    """
    permission_classes = (AllowAny,)
    serializer_class = MyUserSerializer