# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from admin_tools.dashboard import modules


def storage_common():
    return modules.Group(
        _(u'Storage'),
        children=[
            modules.ModelList(_(u'Money'), [
                'src.storage.models.FinanceTransaction',
                'src.storage.models.WalletState',
                'src.storage.models.WalletStateReport',
            ]),
            modules.ModelList(_(u'Static'), [
                'src.storage.models.Recommendation',
            ]),
            modules.ModelList(_(u'Dictionary'), [
                'src.storage.models.Workarea',
                'src.storage.models.JobType',
            ]),
        ])
