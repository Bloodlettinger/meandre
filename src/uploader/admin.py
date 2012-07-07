# -*- coding: utf-8 -*-

from django.contrib import admin

from . import models


class QueueAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'file_type', 'file_size', 'user', 'registered')
    list_filter = ('file_type', 'user')
admin.site.register(models.Queue, QueueAdmin)


class ImageAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'file_type', 'file_size', 'user', 'registered')
    list_filter = ('file_type', 'user')
admin.site.register(models.Image, ImageAdmin)
