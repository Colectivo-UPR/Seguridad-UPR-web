# django
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url

# rest_framework
from rest_framework.authtoken import views as authviews
from rest_framework import routers

#allauth
from allauth.account.views import ConfirmEmailView

# project
from core import views

# router = routers.DefaultRouter()
# # router.register(r'usuarios', views.UserViewSet)
# router.register(r'incidentes', views.IncidentViewSet)
# router.register(r'telefonos', views.PhoneViewSet)
# router.register(r'reportes', views.ReportViewSet)
# router.register(r'servicios', views.ServiceViewSet)
# router.register(r'alertas', views.AlertViewSet)
# router.register(r'userauth',views.AuthUserViewSet)
# router.register(r'officialsphones',views.OfficialsPhonesViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'iupiapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # 
    ###########################
    #   Routes for the staff  #
    ###########################

    # Alerts
    url(r'^create-alert/$', views.AlertCreate.as_view()),
    url(r'^edit-alert/(?P<pk>[0-9]+)/$', views.AlertEdit.as_view()),
    url(r'^send-alert/$',views.send_alert),
    
    # Reports
    url(r'^create-report/$', views.ReportCreate.as_view()),
    url(r'^edit-report/(?P<pk>[0-9]+)/$', views.ReportEdit.as_view()),

    # Phones
    url(r'^create-phone/$', views.PhoneCreate.as_view()),
    url(r'^edit-phone/(?P<pk>[0-9]+)/$', views.PhoneEdit.as_view()),

    # Services
    url(r'^create-service/$', views.ServiceCreate.as_view()),
    url(r'^edit-service/(?P<pk>[0-9]+)/$', views.ServiceEdit.as_view()),

    # Usuarios
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),

    # Usuarios Staff
    # url(r'^register-staff', views.UserStaff.as_view()),
    url(r'^edit-staff-user/(?P<pk>[0-9]+)/$',views.UserEdit.as_view()),
    url(r'^staff-users/$',views.UserList.as_view()),
    url(r'^staff-permissions/(?P<user_email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.staff_permissions),


    # admin
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^', include(router.urls)),

    # Incidentes
    url(r'^incidents/$', views.IncidentList.as_view()),
    url(r'^incidents/(?P<pk>[0-9]+)/$', views.IncidentDetail.as_view()),

    # OfficialPhones
    url(r'^create-official-phone', views.OfficialPhoneCreate.as_view()),
    url(r'^official-phones', views.OfficialPhonesList.as_view()),
    url(r'^edit-official-phone/(?P<pk>[0-9]+)/$', views.OfficialPhonesEdit.as_view()),
    
    ###########################
    #  Routes for all users   #
    ###########################

    #Usuarios
    # url(r'^register',views.UserRegister.as_view()),

    #Incidentes
    url(r'^create-incident', views.IncidentCreate.as_view()),

    # Telefonos
    url(r'^phones/$',views.PhoneList.as_view()),
    url(r'^phones/(?P<pk>[0-9]+)/$', views.PhoneDetail.as_view()),
    
    # Reportes
    url(r'^reports/$', views.ReportList.as_view()),
    url(r'^reports/(?P<pk>[0-9+]+)/$', views.PhoneDetail.as_view()),
    
    # Servicios
    url(r'^services/$', views.ServiceList.as_view()),
    url(r'^services/(?P<pk>[0-9]+)/$', views.ServiceDetail.as_view()),
 
    # Alertas
    url(r'^alerts/', views.AlertList.as_view()),
    url(r'^alerts/(?P<pk>[0-9]+)/$', views.AlertDetail.as_view()),

    # Querellas
    
    url(r'^querellas/$', views.QuerellaListCreateAPIView.as_view()),
    url(r'^querellas/(?P<pk>[0-9]+)/$', views.QuerellaRetrieveUpdateDestroyAPIView.as_view()),
    
    url(r'^querella/area-geografica/$', views.AreaGeograficaListCreateAPIView.as_view()),
    url(r'^querella/area-geografica/(?P<pk>[0-9]+)/$', views.AreaGeograficaRetrieveUpdateDestroyAPIView.as_view()),
    
    url(r'^querella/testigo/$',views.TestigoListCreateAPIView.as_view()),
    url(r'^querella/testigo/(?P<pk>[0-9]+)/$',views.TestigoRetrieveUpdateDestroyAPIView.as_view()),
    
    url(r'^querella/perjudicado/$', views.PerjudicadoListCreateAPIView.as_view()),
    url(r'^querella/perjudicado/(?P<pk>[0-9]+)/$', views.PerjudicadoRetrieveUpdateDestroyAPIView.as_view()),
    
    url(r'^querella/querellado/$', views.QuerelladoListCreateAPIView.as_view()),
    url(r'^querella/querellado/(?P<pk>[0-9]+)/$', views.QuerelladoRetrieveUpdateDestroyAPIView.as_view()),
    
    url(r'^querella/officiales-intervinieron/$', views.OficialesIntervinieronListCreateAPIView.as_view()),
    url(r'^querella/officiales-intervinieron/(?P<pk>[0-9]+)/$', views.OficialesIntervinieronRetrieveUpdateDestroyAPIView.as_view()),
    
    url(r'^querella/sector/$', views.SectorListCreateAPIView.as_view()),
    url(r'^querella/sector/(?P<pk>[0-9]+)/$', views.SectorRetrieveUpdateDestroyAPIView.as_view()),
    
    url(r'^querella/querellante/$', views.QuerellanteListCreateAPIView.as_view()),
    url(r'^querella/querellante/(?P<pk>[0-9]+)/$', views.QuerellanteRetrieveUpdateDestroyAPIView.as_view()),
    
    url(r'^querella/forma-se-refirio/$', views.FormaSeRefirioListCreateAPIView.as_view()),
    url(r'^querella/forma-se-refirio/(?P<pk>[0-9]+)/$', views.FormaSeRefirioRetrieveUpdateDestroyAPIView.as_view()),
    
    url(r'^querella/medio-notificacion/$', views.MedioNotificacionListCreateAPIView.as_view()),
    url(r'^querella/medio-notificacion/(?P<pk>[0-9]+)/$', views.MedioNotificacionRetrieveUpdateDestroyAPIView.as_view()),

    url(r'^querella/tipo-incidente/$', views.TipoIncidenteListCreateAPIView.as_view()),
    url(r'^querella/tipo-incidente/(?P<pk>[0-9]+)/$', views.TipoIncidenteRetrieveUpdateDestroyAPIView.as_view()),

    url(r'^querella/sancion-arresto/$', views.SancionArrestoListCreateAPIView.as_view()),
    url(r'^querella/sancion-arresto/(?P<pk>[0-9]+)/$', views.SancionArrestoRetrieveUpdateDestroyAPIView.as_view()),
    
    # Authenticacion
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^api-token-auth/', authviews.obtain_auth_token),
    # Django Rest Auth
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),

    # Django All Auth
    url(r'^account/', include('allauth.urls')),
    url(r'^account-confirm-email/(?P<key>\w+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
    url(r'^account/email-confirmation-success/',views.ConfirmationSuccess.as_view()),

    # Docs
    url(r'^docs/', include('rest_framework_swagger.urls')),

    # Password Reset
    url(r'^', include('django.contrib.auth.urls')),
    )
urlpatterns += staticfiles_urlpatterns()
