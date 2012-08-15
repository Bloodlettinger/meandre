# -*- coding: utf-8 -*-

import os
import glob

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.contrib.auth.models import User

from tagging.fields import TagField
from tagging.models import Tag, TaggedItem


def upload_by_tag(instance, filename):
    u"""Возвращает путь для загружаемого изображения, учитывая название проекта."""
    return u'uploader/queue/%s/%s' % (instance.tags, filename)


class Queue(models.Model):
    image = models.ImageField(upload_to=upload_by_tag, max_length=256, verbose_name=_(u'Image'))
    file_name = models.CharField(max_length=256, verbose_name=pgettext_lazy(u'uploader', u'Name'))
    file_type = models.CharField(max_length=80, verbose_name=_(u'MIME'))
    file_size = models.IntegerField(verbose_name=pgettext_lazy(u'uploader', u'Size'))
    uploaded_by = models.ForeignKey(User, related_name=u'uploader', verbose_name=pgettext_lazy(u'uploader', u'Uploaded By'))
    confirmed_at = models.DateTimeField(blank=True, null=True)
    confirmed_by = models.ForeignKey(User, related_name=u'confirmer', blank=True, null=True, verbose_name=pgettext_lazy(u'uploader', u'Confirmed By'))
    position = models.IntegerField(null=True, blank=True, verbose_name=_(u'Position'))
    visible = models.BooleanField(default=False, verbose_name=_(u'Visible for anonymous'))
    staff = models.BooleanField(default=False, verbose_name=_(u'Visible for staff'))
    teaser = models.BooleanField(default=False, verbose_name=_(u'Used for presentation'))
    registered = models.DateTimeField(auto_now_add=True)

    tags = TagField()

    class Meta:
        ordering = ('-confirmed_at', '-registered', )
        verbose_name = _(u'Queue Item')
        verbose_name_plural = _(u'Queue Items')

    @staticmethod
    def set_teaser(item):
        tag = Tag.objects.get(name=item.tags)  # у нас только один таг
        id_list = (i.pk for i in TaggedItem.objects.get_by_model(Queue, tag))
        Queue.objects.filter(pk__in=id_list).update(teaser=False)
        item.teaser = True
        item.save()


def delete_image(sender, **kwargs):
    u"""
    Автоматически удаляет изображение при удалении соответствующей модели.

    Сначала удаляем файл, привязанный к модели. Затем удаляем миниатюры.
    """
    model = kwargs.get('instance')
    dir_name = os.path.dirname(model.image.path)
    file_name = os.path.basename(model.image.path)
    model.image.delete(save=False)

    tpl = u'%s/%s/%s*' % (dir_name, settings.THUMBNAIL_SUBDIR, file_name)
    for each in glob.glob(tpl):
        os.remove(each)

models.signals.post_delete.connect(delete_image, sender=Queue, weak=False)
