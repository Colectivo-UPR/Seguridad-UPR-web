from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status, parsers,renderers, permissions, viewsets, generics
from core.serializers import MyUserSerializer, IncidentSerializer, ReportSerializer, PhoneSerializer, ServiceSerializer
from rest_framework.authentication import TokenAuthentication, SessionAuthentication  
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
    API endpoint that allows incidents to be viewed or edited.
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
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication,)
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

    def pre_save(self, obj):
        obj.owner = self.request.user

class IncidentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a incident instance.
    """
    permission_classes = (IsOwnerOnly, IsAuthenticated)
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

    def pre_save(self, obj):
        obj.owner = self.request.user

class UserList(generics.ListAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer

"""
    Routes for clients with TokenAuthentication
"""

class UserRegister(generics.CreateAPIView):
    """
    Register a User
    """
    permission_classes = (AllowAny,)
    serializer_class = MyUserSerializer

class PhoneList(generics.ListAPIView):
    """
    Retrive the Phones list
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer

class PhoneDetail(generics.RetrieveAPIView):
    """
    Retrieve a single phone detail
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer

class ReportList(generics.ListAPIView):
    """
    Retrieve Reports list
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

class ReportDetail(generics.RetrieveAPIView):
    """
    Retrieve a single report detail
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

class ServiceList(generics.ListAPIView):
    """
    Retrieve the list of Services
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceDetail(generics.RetrieveAPIView):
    """
    Retrieve a service detail
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer