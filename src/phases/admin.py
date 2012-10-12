# -*- coding: utf-8 -*-

from django.contrib import admin

from .. custom_admin.admin import ModelTranslationAdmin
from . import models


class PhaseAdmin(ModelTranslationAdmin):
    list_display = ('title', 'position')

admin.site.register(models.Phase, PhaseAdmin)


class StepAdmin(ModelTranslationAdmin):
    list_display = ('title', 'phase', 'price', 'times', 'position')

admin.site.register(models.Step, StepAdmin)
