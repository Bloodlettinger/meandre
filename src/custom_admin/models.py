# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


class WonProjectReport(models.Model):
    u"""
    Фейковая модель для вывода выигранных проектов текущего года.
    """
    class Meta:
        verbose_name = _(u'Won project')
        verbose_name_plural = _(u'Won projects')
        managed = False

