# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import Group


class Company(models.Model):
    u"""
    Модель компаний.
    """
    name = models.CharField(max_length=255, verbose_name=_(u'Name'))
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name=_(u'Address'))
    site = models.URLField(verbose_name=u'Site URL')

    class Meta:
        verbose_name = _(u'Company')
        verbose_name_plural = _(u'Companies')

    def __unicode__(self):
        return self.name


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
    company = models.ForeignKey(Company, blank=True, null=True, verbose_name=_(u'Company'))
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
        name = self.get_full_name()
        if 0 < len(name):
            if self.company:
                return u'%s, %s' % (name, self.company.name)
            else:
                return name
        else:
            return _(u'Person of %s') % self.company.name
