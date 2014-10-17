from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'tsj.views.home', name='home'),
    url(r'^auth/$', 'tsj.views.auth', name='auth'),
    url(r'^admin/', include(admin.site.urls)),
)
