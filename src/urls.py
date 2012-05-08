# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/salmonella/', include('salmonella.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('src.frontend.urls', namespace='frontend')),
)

urlpatterns += staticfiles_urlpatterns()
