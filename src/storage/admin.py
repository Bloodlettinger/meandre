# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.db.models.fields import TextField
from django.db.models.fields.files import ImageField
from django.shortcuts import render_to_response
from django.contrib.admin.templatetags.admin_static import static

from salmonella.admin import SalmonellaMixin
from markitup.widgets import AdminMarkItUpWidget
from easy_thumbnails.widgets import ImageClearableFileInput
from easy_thumbnails.files import get_thumbnailer

from ..custom_admin.admin import ModelTranslationAdmin
from ..custom_admin.options import SortableTabularInline
from ..uploader.models import Queue as ProjectImage
from ..uploader.forms import DoneForm as ImageOptsForm

from . admin_filters import ProjectActiveFilter
from . import models
from . import forms
from . import widgets

PROJECT_CURRENCY_DOLLAR = 2


class WorkareaAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('enabled', )
    search_fields = ('name', )
admin.site.register(models.Workarea, WorkareaAdmin)


class PartnerAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', )
admin.site.register(models.Partner, PartnerAdmin)


class CustomTabularInline(admin.TabularInline):
    template = 'storage/admin/edit_inline/tabular_customer_projects.html'


class ProjectInline(CustomTabularInline):
    model = models.Project
    extra = 0
    fields = ('code', 'short_name', 'reg_date', 'status')
    readonly_fields = ('code', 'short_name', 'reg_date', 'status')
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

    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, ImageField):
            kwargs['widget'] = ImageClearableFileInput
        if db_field.name == 'code':
            kwargs['widget'] = widgets.CustomerCodeWidget
        return super(CustomerAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def workareas(self, item):
        qs = item.workarea.all()
        return u', '.join([i.name for i in qs])
    workareas.short_description = _(u'Work Area')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.change_form_template = 'storage/admin/change_form_customer.html'
        return super(CustomerAdmin, self).change_view(request, object_id, form_url, extra_context)
admin.site.register(models.Customer, CustomerAdmin)


class JobTypeAdmin(ModelTranslationAdmin):
    pass
admin.site.register(models.JobType, JobTypeAdmin)


class MembershipInline(SalmonellaMixin, SortableTabularInline):
    template = 'custom_admin/inline/project_staff_tabular.html'
    model = models.Membership
    extra = 0
    fields = ('role', 'staff', 'position')
    salmonella_fields = ('role', 'staff')


class ProjectAdmin(ModelTranslationAdmin):
    list_display = ('code', 'short_name', 'ptype', 'customer_urlized', 'status_colored', 'begin', 'end', 'price_in_rubs', 'is_public_ru', 'is_public_en', 'reg_date', 'finished_at')
    list_filter = ('ptype', ProjectActiveFilter, 'is_public_ru', 'is_public_en', 'is_archived', 'is_finished', 'in_stats')
    search_fields = ('customer__short_name', 'short_name', 'long_name', 'desc_short', 'desc_long')
    fieldsets = (
        (_(u'Base'), dict(fields=('code', 'customer', 'address', 'short_name', 'long_name', 'ptype', 'status', 'begin', 'end', 'object_square'))),
        (_(u'System'), dict(fields=('reg_date', ))),
        (_(u'State'), dict(fields=('is_public_ru', 'is_public_en', 'is_archived', 'is_finished', 'in_stats'))),
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

    def save_model(self, request, obj, form, change):
        u"""Обеспечивает передачу request в метод `save()` модели."""
        obj.save(request=request)

    def queryset(self, request):
        u"""Подхватываем связанные объекты в одном запросе."""
        return super(ProjectAdmin, self).queryset(request).select_related(depth=1)

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

    def customer_urlized(self, item):
        url = reverse('admin:storage_customer_change', args=(item.customer.pk, ))
        return u'<a href="%s">%s</a>' % (url, item.customer)
    customer_urlized.short_description = _(u'Customer')
    customer_urlized.allow_tags = True

    def status_colored(self, item):
        if item.status == models.PROJECT_STATUS_POTENTIAL:
            color = '#BFBFBF'
        elif item.status == models.PROJECT_STATUS_LOST:
            color = '#DEBFBF'
        elif item.status == models.PROJECT_STATUS_WON:
            if item.is_finished:
                color = '#84C184'
            else:
                color = '#BFDEBF'
        else:
            color = 'red'  # неизвестное состояние
        return u'<div style="background-color: %s;">%s</div>' % (color, item.get_status_display())
    status_colored.short_description = _(u'Status')
    status_colored.allow_tags = True

    def price_in_rubs(self, item):
        if item.currency == PROJECT_CURRENCY_DOLLAR:
            value = item.price_full * item.exchange_rate
        else:
            value = item.price_full
        return u'<span style="float: right;">%.02f</span>' % value
    price_in_rubs.short_description = _(u'Price, rub.')
    price_in_rubs.allow_tags = True

admin.site.register(models.Project, ProjectAdmin)


class MembershipRoleAdmin(ModelTranslationAdmin):
    search_fields = ('title', )
admin.site.register(models.MembershipRole, MembershipRoleAdmin)


class StaffAdmin(ModelTranslationAdmin):
    list_display = ('__unicode__', 'which', 'phone', 'email')
admin.site.register(models.Staff, StaffAdmin)


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


class RecommendationAdmin(ModelTranslationAdmin):
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


class TeaserAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'project', 'begin_date', 'lang', 'visible', 'position')
    list_filter = ('lang', 'visible')
    list_editable = ('visible', 'position', )
    save_on_top = True

    class Media:
        js = (
            static('storage/js/admin_jqueryui.min.js'),
            static('storage/js/admin_list_reorder.js'),
        )
        css = {
            'screen': (
                static('custom_admin/css/style.css'),
            ),
        }

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if obj is None:
            # разрешаем отображать список объектов
            return super(TeaserAdmin, self).has_change_permission(request, obj)
        else:
            # не разрешаем редактировать объекты
            return False

    def has_delete_permission(self, request, obj=None):
        # запрещаем удаление объектов
        return False

    def queryset(self, request):
        WINNED = 2
        return super(TeaserAdmin, self).queryset(request).filter(
            Q(project__is_public_ru=True, lang='ru') | Q(project__is_public_en=True, lang='en'),
            project__status=WINNED,
            project__is_archived=False
            ).order_by('pk')

    def thumbnail(self, item):
        html = u'<img src="%s"/>'
        url = get_thumbnailer(item.project.teaser.image)['uploader_frame'].url
        return html % url
    thumbnail.short_description = _(u'Thumbnail')
    thumbnail.allow_tags = True

    def begin_date(self, item):
        return item.project.begin
    begin_date.short_description = _(u'Begin')

admin.site.register(models.Teaser, TeaserAdmin)
