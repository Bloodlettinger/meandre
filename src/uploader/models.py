# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.contrib.auth.models import User


class Base(models.Model):
    user = models.ForeignKey(User, verbose_name=pgettext_lazy(u'uploader', u'Uploader'))
    file_name = models.CharField(max_length=256, verbose_name=pgettext_lazy(u'uploader', u'Name'))
    file_type = models.CharField(max_length=80, verbose_name=_(u'MIME'))
    file_size = models.IntegerField(verbose_name=pgettext_lazy(u'uploader', u'Size'))
    registered = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-registered', )


class Queue(Base):
    image = models.ImageField(upload_to=u'uploader/queue', max_length=256, verbose_name=_(u'Image'))

    class Meta(Base.Meta):
        verbose_name = _(u'Queue Item')
        verbose_name_plural = _(u'Queue Items')


class Image(Base):
    image = models.ImageField(upload_to=u'uploader/image', max_length=256, verbose_name=_(u'Image'))

    class Meta(Base.Meta):
        verbose_name = _(u'Image Item')
        verbose_name_plural = _(u'Image Items')
