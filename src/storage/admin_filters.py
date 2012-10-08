# -*- coding: utf-8 -*-

from django.db.models import Q
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _

from . import models


class ProjectActiveFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _(u'Status')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('active', _(u'Active')),
            ('potential', _(u'Potential')),
            ('won', _(u'Won')),
            ('lost', _(u'Lost'))
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or 'other')
        # to decide how to filter the queryset.
        if self.value() == 'active':
            return queryset.filter(Q(status=models.PROJECT_STATUS_POTENTIAL) | \
                Q(status=models.PROJECT_STATUS_WON, end__isnull=True))
        if self.value() == 'potential':
            return queryset.filter(status=models.PROJECT_STATUS_POTENTIAL)
        if self.value() == 'won':
            return queryset.filter(status=models.PROJECT_STATUS_WON)
        if self.value() == 'lost':
            return queryset.filter(status=models.PROJECT_STATUS_LOST)
