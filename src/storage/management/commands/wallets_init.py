# -*- coding: utf-8 -*-
from __future__ import absolute_import

from datetime import date, timedelta

from django.db.models import Min
from django.core.management.base import NoArgsCommand
from django.utils.translation import ugettext as _

from ... models import FinanceTransaction as FT
from ... models import WalletState
from ... models import WALLET_TYPE
from ... exceptions import WalletStateNotFound


class Command(NoArgsCommand):

    help = _(u'Initializes the WalletState model.')

    def handle_noargs(self, **options):
        if 0 == WalletState.objects.count():
            if 0 == FT.objects.count():
                print _(u'No financial transactions. Initialize wallets ...')
                moment = date.today().replace(day=1)
            else:
                print _(u'Financial transactions exists. Initialize wallets ...')
                first = FT.objects.aggregate(min=Min('done_at')).get('min')
                moment = first.replace(day=1)

            for key, title in WALLET_TYPE:
                WalletState.objects.create(wallet=key, amount=0, moment=moment)
                print _(u'\t%s initialized on %s.') % (title, moment)
        else:
            print _(u'Wallets are initialized already.')
