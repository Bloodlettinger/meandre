# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin

from modeltranslation.admin import TranslationAdmin
from chunks.admin import ChunkAdmin
from chunks.models import Chunk


class ModelTranslationAdmin(TranslationAdmin):
    class Media:
        js = (
            settings.STATIC_URL + 'modeltranslation/js/force_jquery.js',
            settings.STATIC_URL + 'modeltranslation/js/tabbed_translation_fields.js',
            settings.STATIC_URL + 'js/jquery-ui-1.8.13.custom.min.js',
        )
        css = {
            'screen': (settings.STATIC_URL + 'modeltranslation/css/tabbed_translation_fields.css',),
        }


class ChunkAdmin(ModelTranslationAdmin, ChunkAdmin):
    pass
admin.site.unregister(Chunk)
admin.site.register(Chunk, ChunkAdmin)
