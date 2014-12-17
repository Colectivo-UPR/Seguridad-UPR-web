from django.conf.urls import patterns, include, url
from rest_framework.authtoken import views as authviews
from rest_framework import routers
from core import views
from django.contrib import admin

router = routers.DefaultRouter()
# router.register(r'usuarios', views.UserViewSet)
router.register(r'incidentes', views.IncidentViewSet)
router.register(r'telefonos', views.PhoneViewSet)
router.register(r'reportes', views.ReportViewSet)
router.register(r'servicios', views.ServiceViewSet)
router.register(r'alertas', views.AlertViewSet)
router.register(r'userauth',views.AuthUserViewSet)

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
    
    # Reports
    url(r'^create-report/$', views.ReportCreate.as_view()),
    url(r'^edit-report/(?P<pk>[0-9]+)/$', views.ReportEdit.as_view()),

    # Phones
    url(r'^create-phone/$', views.PhoneCreate.as_view()),
    url(r'^edit-phone/(?P<pk>[0-9]+)/$', views.PhoneEdit.as_view()),

    # Services
    url(r'^create-service/$', views.ServiceCreate.as_view()),
    url(r'^edit-service/$', views.ServiceEdit.as_view()),

    # Usuario
    url(r'^register',views.UserRegister.as_view()),
    url(r'^edit-user',views.UserEdit.as_view()),

    # admin
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    
    ###########################
    #  Routes for all users   #
    ###########################

    # Incidentes
    url(r'^create-incident', views.IncidentCreate.as_view()),
    url(r'^incidents/$', views.IncidentList.as_view()),

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
    
    # Authenticacion
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', authviews.obtain_auth_token)
)