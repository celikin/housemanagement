from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'tsj.views.home', name='home'),
    url(r'^/registration/', 'tsj.views.registration')
    url(r'^/register/', 'tsj.views.register')
    url(r'^admin/', include(admin.site.urls)),
)
