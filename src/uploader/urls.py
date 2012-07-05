# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns('src.uploader.views',
    url(r'^image/$', 'image', name='image'),
)
