from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import serializers, viewsets, routers, permissions
from rest_framework import status
from tsj.models import *
from django.conf import settings
from django.conf.urls.static import static


# Serializers define the API representation.
class CompanySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Company
        fields = ('company_type', 'full_name','post_address','phone','email','boss_fio',
        	'inn','orgn','orgn_date','orgn_emitter','kpp','bill_numb',
        	'bank_name','kor_schet','bik','workgraph')

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    # permission_classes = (permissions.IsAuthenticated, )

class ResidentSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField()
    house = serializers.RelatedField()

    class Meta:
        model = Resident
        fields = ('first_name', 'last_name', 'middle_name', 'flat', 'bill_numb', 'phone', 'user', 'house')

class ResidentViewSet(viewsets.ModelViewSet):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer
    # permission_classes = (permissions.IsAuthenticated,)


class MeterSerializer(serializers.HyperlinkedModelSerializer):
    meter_type = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = MeterReadingHistory


class MeterViewSet(viewsets.ModelViewSet):
    queryset = MeterReadingHistory.objects.all()
    serializer_class = MeterSerializer


# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'company', CompanyViewSet)
router.register(r'user', ResidentViewSet)
router.register(r'meter', MeterViewSet)

urlpatterns = patterns('',

    url(r'^api/', include(router.urls)),
    url(r'^api/auth/$', 'tsj.views.auth_api', name="auth_api"),
    url(r'^api/news/(?P<company_id>\d+)/$', 'tsj.views.news_api', name="news_api"),
    url(r'^$', 'tsj.views.home', name='home'),
    url(r'^org/home/$', 'tsj.views.orghome', name="orghome"),
    url(r'^org/profile/$', 'tsj.views.orgprofile', name="orgprofile"),
    url(r'^profile/$', 'tsj.views.userprofile', name="userprofile"),
    url(r'^auth/$', 'tsj.views.auth', name='auth'),
    url(r'^logout/$', 'tsj.views.logoutview', name='logoutview'),
    url(r'^registration/$', 'tsj.views.registration', name="registration"),
    url(r'^register/$', 'tsj.views.register', name="register"),
    url(r'^org/registration/$', 'tsj.views.orgregistration', name="orgregistration"),
    url(r'^org/houses/$', 'tsj.views.list_houses', name="list_houses"),
    url(r'^org/services/$', 'tsj.views.add_services', name="add_services"),
    url(r'^org/houses/delete/$', 'tsj.views.delete_house', name="delete_house"),
    url(r'^org/houses/add/$', 'tsj.views.add_house', name="add_houses"),
    url(r'^org/create_notification/$', 'tsj.views.create_notification', name="create_notification"),
    url(r'^org/delete_notification/$', 'tsj.views.delete_notification', name="delete_notification"),
    url(r'^org/residents/$', 'tsj.views.list_residents', name="list_residents"),
    url(r'^org/residents/delete/$', 'tsj.views.delete_resident', name="delete_resident"),
    url(r'^org/approve/$', 'tsj.views.userapprove', name="userapprove"),
    url(r'^org/add_services/$', 'tsj.views.add_services', name="add_services"),
    url(r'^org/delete_services/$', 'tsj.views.delete_services', name="delete_services"),
    url(r'^org/add_employer/$', 'tsj.views.add_employer', name="add_employer"),
    url(r'^org/delete_employer/$', 'tsj.views.delete_employer', name="delete_employer"),
    url(r'^org/sendwelcome/(?P<pk>\d+)/$', 'tsj.views.sendwelcome', name="sendwelcome"),
    url(r'^org/sendreject/(?P<pk>\d+)/$', 'tsj.views.sendreject', name="sendreject"),
    url(r'^meter/$', 'tsj.views.meter', name="meter"),
    url(r'^org/houseaccount/(?P<pk>\d+)/$', 'tsj.views.house_account', name="houseaccount"),
    url(r'^employer_request/$', 'tsj.views.employer_request', name="employer_request"),
    url(r'^org/employer_request/$', 'tsj.views.org_employer_request', name="org_employer_request"),
    url(r'^org/delete_emp_req/(?P<pk>\d+)/$', 'tsj.views.delete_emp_req', name="delete_emp_req"),
    url(r'^org/approve_emp_req/(?P<pk>\d+)/$', 'tsj.views.approve_emp_req', name="approve_emp_req"),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
