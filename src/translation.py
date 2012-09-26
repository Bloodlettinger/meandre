# -*- coding: utf-8 -*-

from __future__ import absolute_import

from modeltranslation.translator import translator, TranslationOptions
from chunks.models import Chunk, Media
from . storage import models
from . users.models import Company

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


class JobTypeOpts(TranslationOptions):
    fields = ('short_title', 'long_title', 'description', 'duration')
translator.register(models.JobType, JobTypeOpts)


class StaffOpts(TranslationOptions):
    fields = ('address', 'first_name', 'last_name', 'company')
translator.register(models.Staff, StaffOpts)


class RecommendationOpts(TranslationOptions):
    fields = ('name', )
translator.register(models.Recommendation, RecommendationOpts)


class ChunkOpts(TranslationOptions):
    fields = ('content', )
translator.register(Chunk, ChunkOpts)


class ChunkMediaOpts(TranslationOptions):
    fields = ('title', 'desc', )
translator.register(Media, ChunkMediaOpts)


class CompanyOpts(TranslationOptions):
    fields = ('name', )
translator.register(Company, CompanyOpts)
