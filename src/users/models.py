# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import Group


class CustomGroup(Group):
    u"""
    Модель группы, для удобства.
    """
    class Meta:
        verbose_name = _(u'Group')
        verbose_name_plural = _(u'Groups')
        proxy = True


class CustomUser(User):
    u"""
    Модель пользователя, наследуемая от User. Предназначена для
    хранения дополнительной информации.
    """
    phone = models.CharField(verbose_name=_(u'Phone'), max_length=16,
        blank=True, null=True)
    birth_date = models.DateField(verbose_name=_(u'Birth date'),
        blank=True, null=True)
    sex = models.CharField(verbose_name=_(u'Sex'), max_length=1,
        blank=True, null=True,
        choices=(('M', _(u'Male')), ('F', _(u'Female'))))

    objects = UserManager()

    class Meta:
        verbose_name = _(u'User')
        verbose_name_plural = _(u'Users')
        ordering = ('last_name', 'first_name',)

    def __unicode__(self):
        u"""
        Метод для получения текстового представления экземпляра модели.
        """
        return self.get_full_name()
