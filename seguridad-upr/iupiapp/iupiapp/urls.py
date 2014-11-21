from django.conf.urls import patterns, include, url
from rest_framework.authtoken import views as authviews
from rest_framework import routers
from core import views
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'usuarios', views.UserViewSet)
router.register(r'incidentes', views.IncidentViewSet)
router.register(r'telefonos', views.PhoneViewSet)
router.register(r'reportes', views.ReportViewSet)
router.register(r'servicios', views.ServiceViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'iupiapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    url(r'^incidents/$', views.IncidentList.as_view()),
    url(r'^incidents/(?P<pk>[0-9]+)/$', views.IncidentDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', authviews.obtain_auth_token)
)