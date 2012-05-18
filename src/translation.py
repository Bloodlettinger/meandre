# -*- coding: utf-8 -*-

from modeltranslation.translator import translator, TranslationOptions

from . storage.models import Project


class ProjectTranslationOptions(TranslationOptions):
    u"""
    Класс настроек интернационализации полей модели Project.
    """
    fields = ('address', 'short_name', 'long_name', 'desc_short', 'desc_long',
        'tasks', 'problems', 'results')

translator.register(Project, ProjectTranslationOptions)
