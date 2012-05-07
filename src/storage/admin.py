# -*- coding: utf-8 -*-

from django.contrib import admin
from django.db.models import ManyToManyField
from django.utils.translation import ugettext_lazy as _

from salmonella.admin import SalmonellaMixin

from . import models


class WorkareaAdmin(admin.ModelAdmin):
    list_display = ('name', )
admin.site.register(models.Workarea, WorkareaAdmin)


class PartnerAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', )
admin.site.register(models.Partner, PartnerAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('code', 'short_name', 'partner', 'customer_type', 'partnership_type', 'workareas')
    fieldsets = (
        (_(u'Base'), dict(fields=('code', 'short_name', 'long_name', 'customer_type', 'partnership_type', 'partner', 'workarea', 'url', 'logo'))),
        )
    filter_horizontal = ('workarea', )

    def workareas(self, item):
        qs = item.workarea.all()
        return u', '.join([i.name for i in qs])
    workareas.short_description = _(u'Workarea')

admin.site.register(models.Customer, CustomerAdmin)


class CompanyTeamAdmin(admin.ModelAdmin):
    model = models.CompanyTeam
admin.site.register(models.CompanyTeam, CompanyTeamAdmin)


class JobTypeAdmin(admin.ModelAdmin):
    model = models.JobType
admin.site.register(models.JobType, JobTypeAdmin)


class ProjectImageInline(admin.TabularInline):
    model = models.ProjectImage
    extra = 2


class MembershipInline(SalmonellaMixin, admin.TabularInline):
    model = models.Membership
    extra = 1
    fields = ('role', 'user', 'company', 'url')
    salmonella_fields = ('user', 'role', 'company', )


class ProjectAdmin(SalmonellaMixin, admin.ModelAdmin):
    list_display = ('short_name', 'ptype', 'customer', 'status', 'begin', 'end', 'price_full', 'registered')
    fieldsets = (
        (_(u'Base'), dict(fields=('customer', 'address', 'teaser', 'short_name', 'long_name', 'ptype', 'status', 'begin', 'end', 'object_square'))),
        (_(u'Finance'), dict(fields=('currency', 'exchange_rate', 'price_full', 'price_average'))),
        (_(u'Description'), dict(fields=('desc_short', 'desc_long', 'tasks', 'problems', 'results'))),
        (_(u'Duration'), dict(fields=('duration_production', 'duration_changes', 'duration_discussion', 'duration_other'))),
        (_(u'Jobs'), dict(fields=('job_type', ))),
        )
    inlines = (MembershipInline, ProjectImageInline, )
    search_fields = ('customer', 'short_name', 'long_name', 'desc_short', 'desc_long')
    filter_horizontal = ('job_type', )
    save_on_top = True
    salmonella_fields = ('customer',)

admin.site.register(models.Project, ProjectAdmin)


class FinanceTransactionAdmin(SalmonellaMixin, admin.ModelAdmin):
    list_display = ('amount', 'src', 'dst', 'transaction_type', 'transaction_vat', 'exchange_rate', 'contract', 'contractor', 'done_at')
    salmonella_fields = ('parent', )
admin.site.register(models.FinanceTransaction, FinanceTransactionAdmin)
