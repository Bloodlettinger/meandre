# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import haystack

from . uploader.admin_site import site as uploader_site

haystack.autodiscover()
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/salmonella/', include('salmonella.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^markitup/', include('markitup.urls')),
    url(r'^auth/login/$', 'src.users.views.login'),
    url(r'^auth/', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^sentry/', include('sentry.urls')),
    url(r'^uploader/', include(uploader_site.urls)),
    url(r'^', include('src.frontend.urls', namespace='frontend')),
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
