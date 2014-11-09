from rest_framework import viewsets
from core.serializers import MyUserSerializer, NewsSerializer, ReportSerializer, PhoneSerializer
from core.models import MyUser, News, Report, Phone

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer


class NewsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Noticia to be viewed or edited.
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    
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