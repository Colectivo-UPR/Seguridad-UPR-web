from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import status, parsers,renderers, permissions, viewsets, generics, filters
from core.serializers import IncidentSerializer, ReportSerializer, PhoneSerializer, ServiceSerializer, AlertSerializer, AuthUserSerializer
from rest_framework.authentication import TokenAuthentication, SessionAuthentication  
from core.models import     Incident, Report, Phone, Service, Alert, AuthUser
from core.permissions import IsOwnerOnly


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

class UserList(generics.ListAPIView):
    """
    List users models
    """
    permission_classes = (IsAuthenticated, IsAdminUser,)
    authentication_classes = (TokenAuthentication,)
    queryset = AuthUser.objects.all()
    serializer_class = AuthUserSerializer

class UserEdit(generics.RetrieveUpdateDestroyAPIView):
    """
    Edit users models
    """
    permission_classes = (IsAuthenticated, IsAdminUser,)
    authentication_classes = (IsAuthenticated, IsAdminUser,)
    queryset = AuthUser.objects.all()
    serializer_class = AuthUserSerializer

###############################
#          Phones             #
###############################

class PhoneCreate(generics.CreateAPIView):
    """
    Create a phone
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser,)
    serializer_class = PhoneSerializer

class PhoneEdit(generics.RetrieveUpdateDestroyAPIView):
    """
    Get,Edit,Delete a Report instance
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser,)
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer

###############################
#          Alerts             #
###############################

class AlertCreate(generics.CreateAPIView):
    """
    Create an Alert
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser,)
    serializer_class = AlertSerializer

class AlertEdit(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, Edit, Delete a Alert instance
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,IsAdminUser,)
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer


###############################
#          Reports            #
###############################

class ReportCreate(generics.CreateAPIView):
    """
    Create Reports
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = ReportSerializer

class ReportEdit(generics.RetrieveUpdateDestroyAPIView):
    """
    Get,Edit,Delete a Report instance
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

###############################
#          Services           #
###############################

class ServiceCreate(generics.CreateAPIView):
    """
    Create a service
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, IsAdminUser)
    serializer_class = ServiceSerializer

class ServiceEdit(generics.RetrieveUpdateDestroyAPIView):
    """
    Get,Edit,Delete a Service instance
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, IsAdminUser)
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
    permission_classes = (IsAuthenticated,)
    authentication_classes  = (TokenAuthentication,)
    queryset = Incident.objects.all()
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('incident_date',)
    serializer_class = IncidentSerializer

    def get_queryset(self):
        """
        This view should return only the incidents related to the user
        making the request 
        """
        user = self.request.user
        return Incident.objects.filter(owner=user)


class IncidentDetail(generics.RetrieveAPIView):
    """
    Retrieve, update or delete a incident instance.
    """
    renderer_classes = (renderers.JSONRenderer,)
    permission_classes = (IsOwnerOnly, IsAuthenticated)
    authentication_classes = (TokenAuthentication,)
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    def pre_save(self, obj):
        obj.owner = self.request.user

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



