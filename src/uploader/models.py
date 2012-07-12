# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.contrib.auth.models import User


class Queue(models.Model):
    image = models.ImageField(upload_to=u'uploader/queue', max_length=256, verbose_name=_(u'Image'))
    file_name = models.CharField(max_length=256, verbose_name=pgettext_lazy(u'uploader', u'Name'))
    file_type = models.CharField(max_length=80, verbose_name=_(u'MIME'))
    file_size = models.IntegerField(verbose_name=pgettext_lazy(u'uploader', u'Size'))
    uploaded_by = models.ForeignKey(User, related_name=u'uploader', verbose_name=pgettext_lazy(u'uploader', u'Uploaded By'))
    confirmed_at = models.DateTimeField(blank=True, null=True)
    confirmed_by = models.ForeignKey(User, related_name=u'confirmer', blank=True, null=True, verbose_name=pgettext_lazy(u'uploader', u'Confirmed By'))
    registered = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-registered', )
        verbose_name = _(u'Queue Item')
        verbose_name_plural = _(u'Queue Items')
