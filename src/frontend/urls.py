# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns('src.frontend.views',
    url(r'^$', 'index', name='index'),
    url(r'^search/$', 'search', name='search'),
    url(r'^project/(?P<slug>[-\w]+)/$', 'project', name='project'),
    url(r'^lang/(?P<code>[-a-z]{5})/$', 'lang', name='lang'),
)
