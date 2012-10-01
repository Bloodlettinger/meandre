# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin

from modeltranslation.admin import TranslationAdmin
from chunks import admin as chunkadmin
from chunks import models as chunkmodels


class ModelTranslationAdmin(TranslationAdmin):
    class Media:
        js = (
            'modeltranslation/js/force_jquery.js',
            'modeltranslation/js/column_translation_fields.js',
            'js/jquery-ui-1.8.13.custom.min.js',
        )
        css = {
            'screen': ('modeltranslation/css/column_translation_fields.css',),
        }


class ChunkAdmin(ModelTranslationAdmin, chunkadmin.ChunkAdmin):
    pass
admin.site.unregister(chunkmodels.Chunk)
admin.site.register(chunkmodels.Chunk, ChunkAdmin)


class MediaAdmin(ModelTranslationAdmin, chunkadmin.MediaAdmin):
    pass
admin.site.unregister(chunkmodels.Media)
admin.site.register(chunkmodels.Media, MediaAdmin)
