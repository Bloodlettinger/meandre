# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .. storage import models as storage


class SalesReport(models.Model):
    u"""
    Фейковая модель для вывода выигранных проектов текущего года.
    """
    class Meta:
        verbose_name = _(u'Sales')
        verbose_name_plural = _(u'Sales')
        managed = False

    @staticmethod
    def get_qs():
        qs = storage.Project.objects.filter(
            status=storage.PROJECT_STATUS_WON,
            begin__year=timezone.now().year).order_by('-begin')
        return qs


class ActivityReport(models.Model):
    u"""
    Фейковая модель для вывода активностей.
    """
    class Meta:
        verbose_name = _(u'Activity')
        verbose_name_plural = _(u'Activities')
        managed = False
