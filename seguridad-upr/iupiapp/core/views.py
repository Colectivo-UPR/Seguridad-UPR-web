from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import status, parsers,renderers, permissions, viewsets, generics, filters
from core.serializers import IncidentSerializer, ReportSerializer, PhoneSerializer, ServiceSerializer, AlertSerializer, AuthUserSerializer
from rest_framework.authentication import TokenAuthentication, SessionAuthentication  
from core.models import     Incident, Report, Phone, Service, Alert, AuthUser
from core.permissions import IsOwnerOnly,IsWebAdmin


##########################################
#           API Models Views             #
#           Only Admin Users             #
##########################################      

class IncidentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows incidents to be viewed or edited.
    """
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('pub_date')

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
    API endpoint that allows Service to be viewed or edited.
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class AlertViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Alert to be viewed or edited.
    """
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

class AuthUserViewSet(viewsets.ModelViewSet):
    """
    API endpoinf for the new User model
    """
    queryset = AuthUser.objects.all()
    serializer_class = AuthUserSerializer

    def post_save(self, obj, created=False):
        """
        On creation, replace the raw password with a hashed version.
        """
        if created:
            obj.set_password(obj.password)
            obj.save()

##########################################
#          Admin Views                   #
##########################################

###############################
#          Users              #
###############################

# Create Staff Users

class UserStaff(generics.CreateAPIView):
    """
    Create Staff Users
    """
    renderer_classes = (renderers.JSONRenderer,)
    permission_classes = (IsAuthenticated, IsWebAdmin,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = AuthUserSerializer

    def post_save(self, obj, created=False):
        """
        On creation, replace the raw password with a hashed version.
        """
        if created:
            obj.set_password(obj.password)
            obj.is_webadmin = True
            obj.save()

# View Staff Users
class UserList(generics.ListAPIView):
    """
    List users models
    """
    renderer_classes = (renderers.JSONRenderer,)
    permission_classes = (IsAuthenticated, IsWebAdmin,)
    authentication_classes = (TokenAuthentication,)
    queryset = AuthUser.objects.filter(is_webadmin= True).exclude(is_staff=True)
    serializer_class = AuthUserSerializer

# Edit Staff Users
class UserEdit(generics.RetrieveUpdateDestroyAPIView):
    """
    Edit users models
    """
    renderer_classes = (renderers.JSONRenderer,)
    permission_classes = (IsAuthenticated, IsWebAdmin,)
    authentication_classes = (TokenAuthentication,)
    queryset = AuthUser.objects.filter(is_iswebadmin= True).exclude(is_staff=True)
    serializer_class = AuthUserSerializer

###############################
#          Phones             #
###############################

class PhoneCreate(generics.CreateAPIView):
    """
    Create a phone
    """
    renderer_classes = (renderers.JSONRenderer,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsWebAdmin,)
    serializer_class = PhoneSerializer

class PhoneEdit(generics.RetrieveUpdateDestroyAPIView):
    """
    Get,Edit,Delete a Report instance
    """
    renderer_classes = (renderers.JSONRenderer,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsWebAdmin,)
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer

###############################
#          Alerts             #
###############################

class AlertCreate(generics.CreateAPIView):
    """
    Create an Alert
    """
    renderer_classes = (renderers.JSONRenderer,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsWebAdmin,)
    serializer_class = AlertSerializer

class AlertEdit(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, Edit, Delete a Alert instance
    """
    renderer_classes = (renderers.JSONRenderer,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,IsWebAdmin,)
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

###############################
#          Reports            #
###############################

class ReportCreate(generics.CreateAPIView):
    """
    Create Reports
    """
    renderer_classes = (renderers.JSONRenderer,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsWebAdmin,)
    serializer_class = ReportSerializer

class ReportEdit(generics.RetrieveUpdateDestroyAPIView):
    """
    Get,Edit,Delete a Report instance
    """
    renderer_classes = (renderers.JSONRenderer,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsWebAdmin,)
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

###############################
#          Services           #
###############################

class ServiceCreate(generics.CreateAPIView):
    """
    Create a service
    """
    renderer_classes = (renderers.JSONRenderer,)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, IsWebAdmin,)
    serializer_class = ServiceSerializer

class ServiceEdit(generics.RetrieveUpdateDestroyAPIView):
    """
    Get,Edit,Delete a Service instance
    """
    renderer_classes = (renderers.JSONRenderer,)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, IsWebAdmin,)
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

##########################################
#      Clients/Admin and Views           #
##########################################

class IncidentCreate(generics.CreateAPIView):
    """
    Allow user to create incidents
    """
    renderer_classes = (renderers.JSONRenderer,)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

    def pre_save(self, obj):
        obj.owner = self.request.user

class IncidentList(generics.ListAPIView):
    """
    List all incidents or create a new incident
    """
    renderer_classes = (renderers.JSONRenderer,)
    permission_classes = (IsAuthenticated, IsWebAdmin,)
    authentication_classes  = (TokenAuthentication,)
    queryset = Incident.objects.all()
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('incident_date',)
    serializer_class = IncidentSerializer

class IncidentDetail(generics.RetrieveAPIView):
    """
    Retrieve a incident instance.
    """
    renderer_classes = (renderers.JSONRenderer,)
    permission_classes = (IsAuthenticated, IsWebAdmin,)
    authentication_classes = (TokenAuthentication,)
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

###############################
#          Users              #
###############################

class UserRegister(generics.CreateAPIView):
    """
    Register a User
    """
    renderer_classes = (renderers.JSONRenderer,)
    permission_classes = (AllowAny,)
    serializer_class = AuthUserSerializer

    def post_save(self, obj, created=False):
        """
        On creation, replace the raw password with a hashed version.
        """
        if created:
            obj.set_password(obj.password)
            obj.save()

###############################
#          Phones             #
###############################

class PhoneList(generics.ListAPIView):
    """
    Retrive the Phones list
    """
    renderer_classes = (renderers.JSONRenderer,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer

class PhoneDetail(generics.RetrieveAPIView):
    """
    Retrieve a single phone detail
    """
    renderer_classes = (renderers.JSONRenderer,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer

###############################
#          Reports            #
###############################


class ReportList(generics.ListAPIView):
    """
    Retrieve Reports list
    """
    renderer_classes = (renderers.JSONRenderer,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

class ReportDetail(generics.RetrieveAPIView):
    """
    Retrieve a single report detail
    """
    renderer_classes = (renderers.JSONRenderer,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

###############################
#          Services           #
###############################

class ServiceList(generics.ListAPIView):
    """
    Retrieve the list of Services
    """
    renderer_classes = (renderers.JSONRenderer,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceDetail(generics.RetrieveAPIView):
    """
    Retrieve a service detail
    """
    renderer_classes = (renderers.JSONRenderer,)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

###############################
#          Alerts             #
###############################

class AlertList(generics.ListAPIView):
    """
    Retrieve the list of alerts
    """
    renderer_classes = (renderers.JSONRenderer,)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('pub_date','incident_date')

class AlertDetail(generics.RetrieveAPIView):
    """
    Retrieve an alert detail
    """
    renderer_classes = (renderers.JSONRenderer,)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer



