# -*- coding: utf-8 -*-

from modeltranslation.translator import translator, TranslationOptions
from app.models import Modelka


# class ModelkaTranslationOptions(TranslationOptions):
#     """
#     Класс настроек интернационализации полей модели Modelka.
#     """

#     fields = ('name', 'description',)

# translator.register(Modelka, ModelkaTranslationOptions)