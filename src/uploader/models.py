# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.contrib.auth.models import User

from tagging.fields import TagField


class Queue(models.Model):
    image = models.ImageField(upload_to=u'uploader/queue', max_length=256, verbose_name=_(u'Image'))
    file_name = models.CharField(max_length=256, verbose_name=pgettext_lazy(u'uploader', u'Name'))
    file_type = models.CharField(max_length=80, verbose_name=_(u'MIME'))
    file_size = models.IntegerField(verbose_name=pgettext_lazy(u'uploader', u'Size'))
    uploaded_by = models.ForeignKey(User, related_name=u'uploader', verbose_name=pgettext_lazy(u'uploader', u'Uploaded By'))
    confirmed_at = models.DateTimeField(blank=True, null=True)
    confirmed_by = models.ForeignKey(User, related_name=u'confirmer', blank=True, null=True, verbose_name=pgettext_lazy(u'uploader', u'Confirmed By'))
    position = models.IntegerField(null=True, blank=True, verbose_name=_(u'Position'))
    registered = models.DateTimeField(auto_now_add=True)

    tags = TagField()

    class Meta:
        ordering = ('-confirmed_at', '-registered', )
        verbose_name = _(u'Queue Item')
        verbose_name_plural = _(u'Queue Items')


def delete_image(sender, **kwargs):
    u"""
    Автоматически удаляет изображение при удалении соответствующей модели.

    Сначала удаляем файл, привязанный к модели. Затем удаляем миниатюры.
    """
    import os
    import glob

    model = kwargs.get('instance')
    path = model.image.path
    model.image.delete(save=False)

    # т.к. расширение может изменяться, то ищем файлы, не учитывая его
    short_path = os.path.splitext(path)[0]
    for each in glob.glob(u'%s*' % short_path):
        os.remove(each)

models.signals.post_delete.connect(delete_image, sender=Queue, weak=False)
