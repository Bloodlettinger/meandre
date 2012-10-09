# -*- coding: utf-8 -*-

from django.template.defaultfilters import floatformat
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from admin_tools.utils import AppListElementMixin
from admin_tools.dashboard.modules import DashboardModule

from .. storage import models as storage
from . import models

SALES_LIMIT = 10


class SalesReport(DashboardModule, AppListElementMixin):

    template = 'custom_admin/at_panels/sales.html'
    models = None
    exclude = None
    include_list = None
    exclude_list = None

    def __init__(self, title=None, models=None, exclude=None, **kwargs):
        self.models = list(models or [])
        self.exclude = list(exclude or [])
        self.include_list = kwargs.pop('include_list', [])  # deprecated
        self.exclude_list = kwargs.pop('exclude_list', [])  # deprecated
        super(SalesReport, self).__init__(title, **kwargs)

    def init_with_context(self, context):
        if self._initialized:
            return

        total = 0
        results = []
        for project in models.SalesReport.get_qs():
            data = dict(
                pk=project.pk,
                code=project.code,
                title=project.short_name,
            )
            if project.currency == storage.WALLET_CURRENCY_DOLLARS:
                value = project.price_full * project.exchange_rate
            else:
                value = project.price_full
            data['price'] = value
            total += value
            results.append(data)

        self.children = results[:SALES_LIMIT]
        self._initialized = True

        tpl = _(u'<div style="padding: 4px 8px; font-weight: bold;">Total amount is %s rub.</div>')
        self.pre_content = mark_safe(tpl % floatformat(total, 2))
