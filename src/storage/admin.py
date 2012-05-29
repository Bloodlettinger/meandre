# -*- coding: utf-8 -*-

from django import template
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.db.models.fields.files import ImageField
from django.shortcuts import render_to_response

from easy_thumbnails.widgets import ImageClearableFileInput
from salmonella.admin import SalmonellaMixin
from modeltranslation.admin import TranslationAdmin

from . import models
from . import forms


class WorkareaAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('enabled', )
    search_fields = ('name', )
admin.site.register(models.Workarea, WorkareaAdmin)


class PartnerAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', )
admin.site.register(models.Partner, PartnerAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('code', 'short_name', 'partner', 'customer_type', 'partnership_type', 'workareas')
    list_filter = ('customer_type', 'partnership_type', 'partner')
    search_fields = ('code', 'short_name', 'partner__code', 'partner__name')
    fieldsets = (
        (_(u'Base'), dict(fields=('code', 'short_name', 'long_name', 'customer_type', 'partnership_type', 'partner', 'workarea', 'url', 'logo'))),
        )
    filter_horizontal = ('workarea', )

    def workareas(self, item):
        qs = item.workarea.all()
        return u', '.join([i.name for i in qs])
    workareas.short_description = _(u'Work Area')

admin.site.register(models.Customer, CustomerAdmin)


class CompanyTeamAdmin(admin.ModelAdmin):
    model = models.CompanyTeam
admin.site.register(models.CompanyTeam, CompanyTeamAdmin)


class JobTypeAdmin(admin.ModelAdmin):
    model = models.JobType
admin.site.register(models.JobType, JobTypeAdmin)


class ProjectImageInline(admin.TabularInline):
    model = models.ProjectImage
    formset = forms.ProjectImageInlineFormset
    extra = 1

    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, ImageField):
            kwargs['widget'] = ImageClearableFileInput
        return super(ProjectImageInline, self).formfield_for_dbfield(db_field, **kwargs)


class MembershipInline(SalmonellaMixin, admin.TabularInline):
    model = models.Membership
    extra = 1
    fields = ('role', 'user', 'company', 'url')
    salmonella_fields = ('user', 'role', 'company', )


class ProjectAdmin(SalmonellaMixin, TranslationAdmin):
    list_display = ('short_name', 'ptype', 'customer', 'status', 'begin', 'end', 'price_full', 'is_public', 'registered')
    list_filter = ('ptype', 'status', 'is_public', 'is_archived', 'is_finished', 'in_stats')
    search_fields = ('customer__short_name', 'short_name', 'long_name', 'desc_short', 'desc_long')
    fieldsets = (
        (_(u'Base'), dict(fields=('customer', 'address', 'short_name', 'long_name', 'ptype', 'status', 'begin', 'end', 'object_square'))),
        (_(u'State'), dict(fields=('is_public', 'is_archived', 'is_finished', 'in_stats'))),
        (_(u'Finance'), dict(fields=('currency', 'exchange_rate', 'price_full'))),
        (_(u'Description'), dict(fields=('desc_short', 'desc_long', 'tasks', 'problems', 'results'))),
        (_(u'Duration'), dict(fields=('duration_production', 'duration_changes', 'duration_discussion', 'duration_other'))),
        (_(u'Jobs'), dict(fields=('job_type', ))),
        )
    inlines = (MembershipInline, ProjectImageInline, )
    filter_horizontal = ('job_type', )
    save_on_top = True
    salmonella_fields = ('customer',)

    class Media:
        js = (
            '/static/modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('/static/modeltranslation/css/tabbed_translation_fields.css',),
        }
admin.site.register(models.Project, ProjectAdmin)


class FinanceTransactionAdmin(SalmonellaMixin, admin.ModelAdmin):
    list_display = ('amount', 'wallet', 'transaction_type', 'transaction_vat',
        'exchange_rate', 'user', 'done_at')
    list_filter = ('wallet', 'transaction_type', 'transaction_vat')
    search_fields = ('contract', 'contractor')
    salmonella_fields = ('parent', )
    fieldsets = (
        (None, dict(fields=('parent', 'wallet', 'amount', 'transaction_type', 'transaction_vat', 'exchange_rate', 'description', 'contract', 'contractor'))), )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        obj.save()

    def has_change_permission(self, request, obj=None):
        if obj is None:
            # разрешаем отображать список объектов
            return super(FinanceTransactionAdmin, self).has_change_permission(request, obj)
        else:
            # не разрешаем редактировать объекты
            return False

    def has_delete_permission(self, request, obj=None):
        # запрещаем удаление объектов
        return False

admin.site.register(models.FinanceTransaction, FinanceTransactionAdmin)


class WalletStateAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.WalletState, WalletStateAdmin)


class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
admin.site.register(models.Recommendation, RecommendationAdmin)


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


class WalletStateReportAdmin(BaseReport):
    u"""Вывод текущего состояния счетов."""

    change_list_template = 'storage/report.html'

    def changelist_view(self, request, extra_context=None):
        # убираем ссылку на редактирование объекта
        self.list_display_links = (None, )

        headers = [_(u'Account'), _(u'Balance')]
        qs = models.FinanceTransaction.objects.wallets()

        history = models.WalletState.objects.history()
        graph_data = []
        for item in history:
            value = u'[\'%s\', %f]' % (
                item['moment'].strftime('%Y-%m-%d'), item['amount__sum']
            )
            graph_data.append(value)

        context = dict(
            action_url=reverse('admin:storage_walletstatereport_changelist'),
            app_label=u'Storage',
            model_meta=self.model._meta,
            headers=headers,
            results=qs,
            graph_data=','.join(graph_data)
            )
        context_instance = template.RequestContext(request, current_app=self.admin_site.name)
        return render_to_response(self.change_list_template, context, context_instance=context_instance)

admin.site.register(models.WalletStateReport, WalletStateReportAdmin)
