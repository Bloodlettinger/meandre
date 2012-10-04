# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response

from modeltranslation.admin import TranslationAdmin
from chunks import admin as chunkadmin
from chunks import models as chunkmodels

from .. storage import models as storage
from . import models

PROJECT_STATUS_POTENTIAL = 1
PROJECT_STATUS_WON = 2
PROJECT_CURRENCY_DOLLAR = 2


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


class ChunkAdmin(ModelTranslationAdmin, chunkadmin.ChunkAdmin):
    pass
admin.site.unregister(chunkmodels.Chunk)
admin.site.register(chunkmodels.Chunk, ChunkAdmin)


class MediaAdmin(ModelTranslationAdmin, chunkadmin.MediaAdmin):
    pass
admin.site.unregister(chunkmodels.Media)
admin.site.register(chunkmodels.Media, MediaAdmin)


class BaseReport(admin.ModelAdmin):
    u"""Базовый класс со свойствами для отчётов."""

    def has_add_permission(self, request):
        # запрещаем добавление записей
        return False

    def has_change_permission(self, request, obj=None):
        if obj is None:
            # разрешаем отображать список объектов
            return super(BaseReport, self).has_change_permission(request, obj)
        else:
            # не разрешаем редактировать объекты
            return False

    def has_delete_permission(self, request, obj=None):
        # запрещаем удаление объектов
        return False


class WonProjectReportAdmin(BaseReport):
    u"""Вывод списка выигранных проектов за текущий год."""

    change_list_template = 'custom_admin/reports/won_projects.html'

    def changelist_view(self, request, extra_context=None):
        # убираем ссылку на редактирование объекта
        self.list_display_links = (None, )

        headers = [_(u'Project'), _(u'Begin'), _(u'Price, Rub')]
        qs = storage.Project.objects.filter(status=PROJECT_STATUS_WON, begin__year=timezone.now().year)
        total = 0
        results = []
        for project in qs:
            data = dict(title=project.short_name, end=project.end)
            if project.currency == PROJECT_CURRENCY_DOLLAR:
                value = project.price_full * project.exchange_rate
            else:
                value = project.price_full
            data['price'] = value
            results.append(data)
            total += value

        context = dict(
            #action_url=reverse('admin:custom_admin_wonprojectreport_changelist'),
            app_label=u'Reports',
            model_meta=self.model._meta,
            headers=headers,
            results=results,
            total=total
            )
        context_instance = template.RequestContext(request, current_app=self.admin_site.name)
        return render_to_response(self.change_list_template, context, context_instance=context_instance)

admin.site.register(models.WonProjectReport, WonProjectReportAdmin)


class ActivityReportAdmin(BaseReport):
    u"""Вывод списка активностей."""

    class Media:
        css = {
            'screen': ('custom_admin/css/activity.css', ),
        }

    change_list_template = 'custom_admin/reports/activities.html'

    def changelist_view(self, request, extra_context=None):
        # убираем ссылку на редактирование объекта
        self.list_display_links = (None, )

        qs = storage.Project.objects.select_related(depth=1).filter(status__in=(PROJECT_STATUS_POTENTIAL, PROJECT_STATUS_WON))

        context = dict(
            #action_url=reverse('admin:custom_admin_wonprojectreport_changelist'),
            app_label=u'Reports',
            model_meta=self.model._meta,
            projects=qs
            )
        context_instance = template.RequestContext(request, current_app=self.admin_site.name)
        return render_to_response(self.change_list_template, context, context_instance=context_instance)

admin.site.register(models.ActivityReport, ActivityReportAdmin)
