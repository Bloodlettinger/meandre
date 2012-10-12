# -*- coding: utf-8 -*-

from django.contrib import admin

from . import models


class PhaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'position')

admin.site.register(models.Phase, PhaseAdmin)


class StepAdmin(admin.ModelAdmin):
    list_display = ('title', 'phase', 'price', 'times', 'position')

admin.site.register(models.Step, StepAdmin)
