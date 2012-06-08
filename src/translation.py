# -*- coding: utf-8 -*-

from __future__ import absolute_import

from modeltranslation.translator import translator, TranslationOptions

from . storage import models

u"""
Модуль содержит настройки интернационализации для полей моделей.
"""


class ProjectOpts(TranslationOptions):
    fields = ('address', 'short_name', 'long_name', 'desc_short', 'desc_long',
        'tasks', 'problems', 'results')
translator.register(models.Project, ProjectOpts)


class MembershipRoleOpts(TranslationOptions):
    fields = ('title', )
translator.register(models.MembershipRole, MembershipRoleOpts)
