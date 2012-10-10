# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.shortcuts import render_to_response

from modeltranslation.admin import TranslationAdmin
from chunks import admin as chunkadmin
from chunks import models as chunkmodels

from .. storage import models as storage
from . import ddmmyy
from . import models


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


class SalesReportAdmin(BaseReport):
    u"""Вывод списка выигранных проектов за текущий год."""
    list_display = ('code', 'short_name', 'partner_with_type', 'begin_dmy', 'end_dmy', 'price_in_rubs')
    list_filter = ('customer__customer_type', )
    change_list_template = 'custom_admin/changelist/sales.html'

    def queryset(self, request):
        u"""обеспечивает выборку дополнительных данных"""
        qs = super(SalesReportAdmin, self).queryset(request)
        return qs.select_related()

    def price_in_rubs(self, item):
        if item.currency == storage.WALLET_CURRENCY_DOLLARS:
            value = item.price_full * item.exchange_rate
        else:
            value = item.price_full
        return u'<span style="float: right;">%.02f</span>' % value
    price_in_rubs.short_description = _(u'Price, rub.')
    price_in_rubs.allow_tags = True

    def partner_with_type(self, item):
        tpl = u'%(partner)s %(ptype)s'
        partner = item.customer.partner
        if partner is None:
            partner = u'--'
        parthership = item.customer.partnership_type
        params = dict(
            partner=partner,
            ptype=storage.PARTNERSHIP_SIGNS.get(parthership, '&nbsp;')
        )
        return mark_safe(tpl % params)
    partner_with_type.short_description = _(u'Partner')
    partner_with_type.allow_tags = True

    def begin_dmy(self, item):
        return ddmmyy(item.begin)
    begin_dmy.short_description = _(u'Begin')

    def end_dmy(self, item):
        return ddmmyy(item.end)
    end_dmy.short_description = _(u'End')

admin.site.register(models.SalesReport, SalesReportAdmin)


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

        qs = storage.Project.objects.select_related(depth=1).filter(
            status__in=(storage.PROJECT_STATUS_POTENTIAL, storage.PROJECT_STATUS_WON),
            end__isnull=True
        )

        context = dict(
            #action_url=reverse('admin:custom_admin_activityreport_changelist'),
            app_label=_(u'Reports'),
            model_meta=self.model._meta,
            projects=qs
            )
        context_instance = template.RequestContext(request, current_app=self.admin_site.name)
        return render_to_response(self.change_list_template, context, context_instance=context_instance)

admin.site.register(models.ActivityReport, ActivityReportAdmin)
