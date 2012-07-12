# -*- coding: utf-8 -*-

from django.contrib.admin.sites import AdminSite
from django.views.decorators.cache import never_cache
from django.template.response import TemplateResponse

from . import views
from . import models
from . import forms


class UploaderAdmin(AdminSite):

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url
        urls = patterns(
            '',
            url(r'^library/$', self.admin_view(self.library), name="library"),
            url(r'^image/$', views.image, name='image'),
            url(r'^done/$', views.done, name='done'),
            )
        urls += super(UploaderAdmin, self).get_urls()
        return urls

    def has_permission(self, request):
        return request.user.is_active

    @never_cache
    def library(self, request, extra_context=None):
        context = dict(
            form=forms.DoneForm(),
            queue_list=models.Queue.objects.filter(confirmed_by__isnull=True),
            image_list=models.Queue.objects.exclude(confirmed_by__isnull=True)
            )
        return TemplateResponse(request, 'uploader/layout.html', context)

site = UploaderAdmin(name=u'uploader')
