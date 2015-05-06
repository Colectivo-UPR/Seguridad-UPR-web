# python
import json
import boto3
import awscli

# django
from django.views.generic import TemplateView
from django.db.models import Q

# rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import status, parsers,renderers, permissions, viewsets, generics, filters
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes, renderer_classes
from rest_framework import status, mixins

# project
from core.serializers import *
from core.models import *
from core.permissions import IsOwnerOnly,IsWebAdmin, IsDirector, IsStaff
from iupiapp import settings

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
    API endpoint for the new User model
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

class OfficialsPhonesViewSet(viewsets.ModelViewSet):
    """
    API endpoint for the OfficialPhones Model
    """
    queryset = OfficialsPhones.objects.all()
    serializer_class = OfficialsPhonesSerializer

##########################################
#          Admin Views                   #
##########################################

###############################
#          Users              #
###############################
# View user info by id
class UserDetail(generics.RetrieveAPIView):
    renderer_classes = (renderers.JSONRenderer,)
    permission_classes = (IsAuthenticated, IsStaff,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = AuthUserSerializer
    queryset = AuthUser.objects.all()



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
            obj.is_official = True
            obj.save()

# View Staff Users
class UserList(generics.ListAPIView):
    """
    List users models
    """
    renderer_classes = (renderers.JSONRenderer,renderers.BrowsableAPIRenderer,)
    permission_classes = (IsAuthenticated, IsWebAdmin,)
    authentication_classes = (TokenAuthentication, SessionAuthentication,)
    resultquery = AuthUser.objects.filter(is_official= True) | AuthUser.objects.filter(is_shift_manager=True) | AuthUser.objects.filter(is_director=True)
    queryset = resultquery.exclude(is_staff=True)
    serializer_class = AuthUserStaffListSerializer

# Edit Staff Users
class UserEdit(generics.RetrieveUpdateDestroyAPIView):
    """
    Edit users models
    """
    renderer_classes = (renderers.JSONRenderer,)
    permission_classes = (IsAuthenticated, IsWebAdmin,)
    authentication_classes = (TokenAuthentication,)
    queryset = AuthUser.objects.filter(is_official= True).exclude(is_staff=True)
    serializer_class = AuthUserDetailSerializer

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsStaff])
@renderer_classes([renderers.JSONRenderer])
def send_alert(request):
    sns = boto3.client('sns')
    msg = request.POST['msg']
    response  = sns.list_endpoints_by_platform_application(PlatformApplicationArn=settings.appArn)
    endpoints = response['Endpoints']

    for endpoint in endpoints:
        e = endpoint['EndpointArn']
        post_response = sns.publish(Message=msg, TargetArn=e)
    
        if post_response['ResponseMetadata']['HTTPStatusCode'] == 200: 
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# Modify user permission
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsDirector])
@renderer_classes([renderers.JSONRenderer])
def staff_permissions(request,user_email):
    """
    Assign user staff permissions
    """
    try:
        # Validate exist user with email
        user = AuthUser.objects.get(email=user_email)

    except AuthUser.DoesNotExist:
        # return not user found
        return Response({"non_field_errors": "email provided not match a valid user"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # validate json data
        json_data = json.loads(request.body)

    except ValueError as e:
        return Response({"non_field_errors": "Invalid json format: %s" % e},status=status.HTTP_400_BAD_REQUEST)

    try:
        # check all values of the json are bool type and that the keys are correct.
        if type(json_data['is_director']) and type(json_data['is_shift_manager']) and type(json_data['is_official'])  == bool:

            # Update the user permissions
            user.is_director = json_data['is_director']
            user.is_shift_manager = json_data['is_shift_manager']
            user.is_official = json_data['is_official']
            user.save()

        else:
            raise KeyError("JSON keys values must be <bool> type")
        
    except KeyError as e:
        # Return Error message
       
        return Response({"non_field_errors": 'Invalid json keys:values: "is_director": <bool>,"is_shift_manager": <bool>,"is_official": <bool>' % e},status=status.HTTP_400_BAD_REQUEST)

    return Response({"details":"ok"}, status=status.HTTP_200_OK)

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

###############################
#     Officials Phones        #
###############################

class OfficialPhoneCreate(generics.CreateAPIView):
    """
    Create an Official Phone
    """
    renderer_classes = (renderers.JSONRenderer,)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, IsWebAdmin,)
    serializer_class = OfficialsPhonesSerializer

class OfficialPhonesList(generics.ListAPIView):
    """
    List Officials Phones
    """

    redenderer_classes = (renderers.JSONRenderer,)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, IsWebAdmin,)
    queryset = OfficialsPhones.objects.all()
    serializer_class = OfficialsPhonesSerializer

class OfficialPhonesEdit(generics.RetrieveUpdateDestroyAPIView):
    """
    Modify the officials phones
    """
    renderer_classes = (renderers.JSONRenderer,)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, IsWebAdmin,)
    queryset = OfficialsPhones.objects.all()
    serializer_class = OfficialsPhonesSerializer
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

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

class IncidentList(generics.ListAPIView):
    """
    List all incidents or create a new incident
    """
    renderer_classes = (renderers.JSONRenderer,)
    permission_classes = (IsAuthenticated, IsWebAdmin,)
    authentication_classes   = (TokenAuthentication,)
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

    def pre_save(self, obj):
        obj.user_id = self.request.user

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


##################################
#       Confirmation Success     #
##################################
class ConfirmationSuccess(TemplateView):
    template_name= "confirmation_success.html"


##################################
#       Querellas Routes         #
##################################

class QuerellaListCreateAPIView(generics.ListCreateAPIView):

    queryset = Querella.objects.all()
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer,)
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    permission_classes = (IsAuthenticated, IsDirector,)
    serializer_class = QuerellaSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('numero_caso',)

    paginate_by = None
    paginate_by_param = 'page_size'
    # Set MAX results per page
    max_paginate_by = None


class QuerellaRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Querella.objects.all()
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer,)
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    permission_classes = (IsAuthenticated, IsDirector,)
    serializer_class = QuerellaSerializer

class AreaGeograficaListCreateAPIView(generics.ListCreateAPIView):

    queryset = AreaGeografica.objects.all()
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer,)
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    permission_classes = (IsAuthenticated, IsDirector,)
    serializer_class = AreaGeograficaSerializer

class AreaGeograficaRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AreaGeografica.objects.all()
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer,)
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    permission_classes = (IsAuthenticated, IsDirector,)
    serializer_class = AreaGeograficaSerializer

class TestigoListCreateAPIView(generics.ListCreateAPIView):

    queryset = Testigo.objects.all()
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer,)
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    permission_classes = (IsAuthenticated, IsDirector,)
    serializer_class = TestigoSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('id_querella',)

class TestigoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Testigo.objects.all()
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer,)
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    permission_classes = (IsAuthenticated, IsDirector,)
    serializer_class = TestigoSerializer

class PerjudicadoListCreateAPIView(generics.ListCreateAPIView):

    queryset = Perjudicado.objects.all()
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer,)
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    permission_classes = (IsAuthenticated, IsDirector,)
    serializer_class = PerjudicadoSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('id_querella',)

class PerjudicadoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Perjudicado.objects.all()
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer,)
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    permission_classes = (IsAuthenticated, IsDirector,)
    serializer_class = PerjudicadoSerializer

class QuerelladoListCreateAPIView(generics.ListCreateAPIView):

    queryset = Querellado.objects.all()
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer,)
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    permission_classes = (IsAuthenticated, IsDirector,)
    serializer_class = QuerelladoSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('id_querella',)

class QuerelladoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Querellado.objects.all()
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer,)
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    permission_classes = (IsAuthenticated, IsDirector,)
    serializer_class = QuerelladoSerializer

class OficialesIntervinieronListCreateAPIView(generics.ListCreateAPIView):

    queryset = OficialesIntervinieron.objects.all()
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer,)
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    permission_classes = (IsAuthenticated, IsDirector,)
    serializer_class = OficialesIntervinieronSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('id_querella',)

class OficialesIntervinieronRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = OficialesIntervinieron.objects.all()
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer,)
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    permission_classes = (IsAuthenticated, IsDirector,)
    serializer_class = OficialesIntervinieronSerializer

class SectorListCreateAPIView(generics.ListCreateAPIView):

    queryset = Sector.objects.all()
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer,)
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    permission_classes = (IsAuthenticated, IsDirector,)
    serializer_class = SectorSerializer

class SectorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Sector.objects.all()
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer,)
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    permission_classes = (IsAuthenticated, IsDirector,)
    serializer_class = SectorSerializer

class QuerellanteListCreateAPIView(generics.ListCreateAPIView):

    queryset = Querellante.objects.all()
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer,)
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    permission_classes = (IsAuthenticated, IsDirector,)
    serializer_class = QuerellanteSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('id_querella',)

class QuerellanteRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Querellante.objects.all()
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer,)
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    permission_classes = (IsAuthenticated, IsDirector,)
    serializer_class = QuerellanteSerializer

class FormaSeRefirioListCreateAPIView(generics.ListCreateAPIView):

    queryset = FormaSeRefirio.objects.all()
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer,)
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    permission_classes = (IsAuthenticated, IsDirector,)
    serializer_class = FormaSeRefirioSerializer

class FormaSeRefirioRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = FormaSeRefirio.objects.all()
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer,)
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    permission_classes = (IsAuthenticated, IsDirector,)
    serializer_class = FormaSeRefirioSerializer

class MedioNotificacionListCreateAPIView(generics.ListCreateAPIView):

    queryset = MedioNotificacion.objects.all()
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer,)
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    permission_classes = (IsAuthenticated, IsDirector,)
    serializer_class = MedioNotificacionSerializer

class MedioNotificacionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = MedioNotificacion.objects.all()
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer,)
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    permission_classes = (IsAuthenticated, IsDirector,)
    serializer_class = MedioNotificacionSerializer

class TipoIncidenteListCreateAPIView(generics.ListCreateAPIView):

    queryset = TipoIncidente.objects.all()
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer,)
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    permission_classes = (IsAuthenticated, IsDirector,)
    serializer_class = TipoIncidenteSerializer

class TipoIncidenteRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = TipoIncidente.objects.all()
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer,)
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    permission_classes = (IsAuthenticated, IsDirector,)
    serializer_class = TipoIncidenteSerializer

class SancionArrestoListCreateAPIView(generics.ListCreateAPIView):

    queryset = SancionArresto.objects.all()
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsDirector,)
    serializer_class = SancionArrestoSerializer

class SancionArrestoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = SancionArresto.objects.all()
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsDirector,)
    serializer_class = SancionArrestoSerializer
