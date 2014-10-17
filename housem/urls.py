from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import serializers, viewsets, routers, permissions
from tsj.models import *

# Serializers define the API representation.
class CompanySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Company
        fields = ('company_type', 'full_name','post_adress','phone','email','boss_fio',
        	'inn','orgn','orgn_date','orgn_emitter','kpp','bill_numb',
        	'bank_name','kor_schet','bik','workgraph')

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (permissions.IsAuthenticated, )

class ResidentSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField()
    house = serializers.RelatedField()

    class Meta:
        model = Resident
        fields = ('fio', 'flat', 'lnumb', 'phone', 'user', 'house')

class ResidentViewSet(viewsets.ModelViewSet):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer
    permission_classes = (permissions.IsAuthenticated,)

# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'residents', ResidentViewSet)

urlpatterns = patterns('',
    # Examples:
    url(r'^api/', include(router.urls)),
    url(r'^$', 'tsj.views.home', name='home'),
    url(r'^auth/$', 'tsj.views.auth', name='auth'),
    url(r'^registration/$', 'tsj.views.registration'),
    url(r'^register/', 'tsj.views.register'),
    url(r'^admin/', include(admin.site.urls)),
)

