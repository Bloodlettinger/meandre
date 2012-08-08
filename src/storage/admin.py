# -*- coding: utf-8 -*-

from django import template
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.db.models.fields import TextField
from django.shortcuts import render_to_response

from salmonella.admin import SalmonellaMixin
from markitup.widgets import AdminMarkItUpWidget

from ..custom_admin.admin import ModelTranslationAdmin
from ..uploader.models import Queue as ProjectImage
from ..uploader.forms import DoneForm as ImageOptsForm

from . import models
from . import forms
from . import widgets


class WorkareaAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('enabled', )
    search_fields = ('name', )
admin.site.register(models.Workarea, WorkareaAdmin)


class PartnerAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', )
admin.site.register(models.Partner, PartnerAdmin)


class CustomTabularInline(admin.TabularInline):
    template = 'storage/admin/edit_inline/tabular.html'


class ProjectInline(CustomTabularInline):
    model = models.Project
    extra = 0
    fields = ('code', 'short_name', 'registered', 'status')
    readonly_fields = ('code', 'short_name', 'registered', 'status')
    can_delete = False

    def has_add_permission(self, request):
        return False


class CustomerAdmin(ModelTranslationAdmin):
    list_display = ('code', 'short_name', 'partner', 'customer_type', 'partnership_type', 'workareas')
    list_filter = ('customer_type', 'partnership_type', 'partner')
    search_fields = ('code', 'short_name', 'partner__code', 'partner__name')
    fieldsets = (
        (_(u'Base'), dict(fields=('code', 'short_name', 'long_name', 'customer_type', 'partnership_type', 'partner', 'workarea', 'url', 'logo'))),
        )
    filter_horizontal = ('workarea', )
    inlines = (ProjectInline, )

    def workareas(self, item):
        qs = item.workarea.all()
        return u', '.join([i.name for i in qs])
    workareas.short_description = _(u'Work Area')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.change_form_template = 'storage/admin/change_form_customer.html'
        return super(CustomerAdmin, self).change_view(request, object_id, form_url, extra_context)
admin.site.register(models.Customer, CustomerAdmin)


class JobTypeAdmin(admin.ModelAdmin):
    model = models.JobType
admin.site.register(models.JobType, JobTypeAdmin)


class MembershipInline(SalmonellaMixin, admin.TabularInline):
    model = models.Membership
    extra = 1
    fields = ('role', 'user')
    salmonella_fields = ('user', 'role')


class ProjectAdmin(ModelTranslationAdmin):
    list_display = ('code', 'short_name', 'ptype', 'customer', 'status', 'begin', 'end', 'price_full', 'is_public', 'registered')
    list_filter = ('ptype', 'status', 'is_public', 'is_archived', 'is_finished', 'in_stats')
    search_fields = ('customer__short_name', 'short_name', 'long_name', 'desc_short', 'desc_long')
    fieldsets = (
        (_(u'Base'), dict(fields=('code', 'customer', 'address', 'short_name', 'long_name', 'ptype', 'status', 'begin', 'end', 'object_square'))),
        (_(u'System'), dict(fields=('registered', ))),
        (_(u'State'), dict(fields=('is_public', 'is_archived', 'is_finished', 'in_stats'))),
        (_(u'Finance'), dict(fields=('currency', 'exchange_rate', 'price_full'))),
        (_(u'Description'), dict(fields=('desc_short', 'desc_long', 'tasks', 'problems', 'results'))),
        (_(u'Duration'), dict(fields=('duration_production', 'duration_changes', 'duration_discussion', 'duration_other'))),
        (_(u'Jobs'), dict(fields=('job_type', ))),
        )
    inlines = (MembershipInline, )
    filter_horizontal = ('job_type', )
    save_on_top = True
    form = forms.ProjectForm
    formfield_overrides = {TextField: {'widget': AdminMarkItUpWidget}}

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'desc_short':
            kwargs['widget'] = widgets.TeaserPreviewWidget
        elif db_field.name == 'ptype':
            kwargs['widget'] = widgets.RadioSelectHorizontal
            kwargs['choices'] = models.PROJECT_TYPE_ICONS
        elif db_field.name == 'status':
            kwargs['widget'] = widgets.RadioSelectHorizontal
        elif db_field.name == 'currency':
            kwargs['widget'] = widgets.CurrencySelect
        return super(ProjectAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def add_view(self, request, form_url='', extra_context=None):
        if extra_context is None:
            extra_context = dict()
        extra_context.update(
            dict(dropzone_visible=False))
        return super(ProjectAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.change_form_template = 'storage/admin/change_form_project.html'

        code = self.model.objects.get(pk=object_id).code.lower()
        images = ProjectImage.objects.filter(tags=code).order_by('position')
        formset = forms.ImagePositionFormSet(request.POST or None, prefix='images_set', queryset=images)
        if request.method == 'POST':
            if formset.is_valid():
                formset.save()

        if extra_context is None:
            extra_context = dict()
        extra_context.update(
            dict(
                dropzone_visible=True,
                uploader_form=ImageOptsForm(),
                tag=code,
                image_fs=formset,
                image_list=images))
        return super(ProjectAdmin, self).change_view(request, object_id, form_url, extra_context)

admin.site.register(models.Project, ProjectAdmin)


class MembershipRoleAdmin(ModelTranslationAdmin):
    search_fields = ('title', )
admin.site.register(models.MembershipRole, MembershipRoleAdmin)


class FinanceTransactionAdmin(SalmonellaMixin, admin.ModelAdmin):
    list_display = ('wallet', 'type_color', 'contractor', 'contract', 'amount',
            'transaction_vat', 'done_at')
    list_filter = ('wallet', 'transaction_type', 'transaction_vat')
    search_fields = ('contract', 'contractor')
    salmonella_fields = ('parent', )
    fieldsets = (
        (None, dict(fields=('done_at', 'transaction_type', 'amount', 'transaction_vat', 'wallet', 'description', 'contract', 'contractor', 'parent'))), )

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

    def type_color(self, item):
        colors = {1: "#458069", 2: "#AD479C"}
        tpl = """<div style="text-align: center; padding:2px 4px; background-color: %s;">%s</div>"""
        return tpl % (
            colors.get(item.transaction_type, "gray"),
            item.get_transaction_type_display()
            )
    type_color.short_model_desc = _(u'Type')
    type_color.allow_tags = True
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
