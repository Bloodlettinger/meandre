# -*- coding: utf-8 -*-

from django.contrib.admin.sites import AdminSite
from django.views.decorators.cache import never_cache
from django.template.response import TemplateResponse

from . import views
from . import models


class UploaderAdmin(AdminSite):

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url
        urls = patterns(
            '',
            url(r'^image/$', views.image, name='image'),
            url(r'^library/$', self.admin_view(self.library), name="library"),
            )
        urls += super(UploaderAdmin, self).get_urls()
        return urls

    def has_permission(self, request):
        return request.user.is_active

    @never_cache
    def library(self, request, extra_context=None):
        context = dict(
            queue_list=models.Queue.objects.all(),
            image_list=models.Image.objects.all()
            )
        return TemplateResponse(request, 'uploader/layout.html', context)

site = UploaderAdmin(name=u'uploader')
