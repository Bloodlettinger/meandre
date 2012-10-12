# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Phase(models.Model):
    u"""
    """
    title = models.CharField(max_length=255, verbose_name=_(u'Title'))
    position = models.PositiveIntegerField(default=0, verbose_name=_(u'Position'), help_text=_(u'Hide this field.'))

    class Meta:
        verbose_name = _(u'Phase')
        verbose_name_plural = _(u'Phases')
        ordering = ('position', )

    def __unicode__(self):
        return u'%i. %s' % (self.position, self.title)


class Step(models.Model):
    u"""
    Определяет значения элементов фаз проекта по умолчанию.
    """
    phase = models.ForeignKey(Phase, verbose_name=_(u'Phase'))
    title = models.CharField(max_length=255, verbose_name=_(u'Title'))
    price = models.PositiveIntegerField(default=0, verbose_name=_(u'Cost per Hour'))
    times = models.FloatField(default=1.0, verbose_name=_(u'Coefficient'))
    position = models.PositiveIntegerField(default=0, verbose_name=_(u'Position'), help_text=_(u'Hide this field.'))

    class Meta:
        verbose_name = _(u'Step')
        verbose_name_plural = _(u'Steps')
        ordering = ('position', )

    def __unicode__(self):
        return self.title


class Relation(models.Model):
    u"""
    Определяет фазы для проекта.
    """
    project = models.ForeignKey('storage.Project')
    phase = models.ForeignKey(Step)
    duration_a = models.PositiveIntegerField()
    duration_b = models.PositiveIntegerField()
    cost = models.PositiveIntegerField()
