# -*- coding: utf-8 -*-

from __future__ import absolute_import

from modeltranslation.translator import translator, TranslationOptions
from chunks.models import Chunk

from . storage import models

u"""
Модуль содержит настройки интернационализации для полей моделей.
"""


class ProjectOpts(TranslationOptions):
    fields = ('address', 'short_name', 'long_name', 'desc_short', 'desc_long',
        'tasks', 'problems', 'results')
translator.register(models.Project, ProjectOpts)


class CustomerOpts(TranslationOptions):
    fields = ('short_name', 'long_name')
translator.register(models.Customer, CustomerOpts)


class MembershipRoleOpts(TranslationOptions):
    fields = ('title', )
translator.register(models.MembershipRole, MembershipRoleOpts)


class ChunkOpts(TranslationOptions):
    fields = ('content', )
translator.register(Chunk, ChunkOpts)
