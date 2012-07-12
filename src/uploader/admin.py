# -*- coding: utf-8 -*-

from django.contrib import admin

from . import models


class QueueAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'file_type', 'file_size', 'uploaded_by', 'registered', 'confirmed_by', 'confirmed_at')
    list_filter = ('file_type', 'uploaded_by', 'confirmed_by')
admin.site.register(models.Queue, QueueAdmin)
