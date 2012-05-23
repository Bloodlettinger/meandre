# -*- coding: utf-8 -*-
from __future__ import absolute_import

from datetime import date
from decimal import Decimal
from dateutil.rrule import rrule
from dateutil.rrule import MONTHLY
from dateutil.relativedelta import relativedelta as RD

from django.db.models import Max, Sum
from django.core.management.base import NoArgsCommand
from django.utils.translation import ugettext as _

from ... models import FinanceTransaction as FT
from ... models import WalletState
from ... models import WALLET_TYPE

INCOME = 1
EXPENSE = 2


class Command(NoArgsCommand):

    help = _(u'Fills the WalletState model.')

    def handle_noargs(self, **options):
        if 0 == WalletState.objects.count():
            print _(u'Use `wallets_init` first.')
        else:
            start = WalletState.objects.aggregate(max=Max('moment')).get('max')
            for begin in rrule(MONTHLY, dtstart=start, until=date.today() + RD(months=-1)):
                print begin
                for key, title in WALLET_TYPE:
                    income = FT.objects.filter(
                        done_at__year=begin.year,
                        done_at__month=begin.month,
                        wallet=key,
                        transaction_type=INCOME
                    ).aggregate(sum=Sum('amount')).get('sum') or 0.0
                    expense = FT.objects.filter(
                        done_at__year=begin.year,
                        done_at__month=begin.month,
                        wallet=key,
                        transaction_type=EXPENSE
                    ).aggregate(sum=Sum('amount')).get('sum') or 0.0

                    state = WalletState.objects.get(wallet=key, moment=begin)
                    #print income, expense, state.amount, Decimal(str(income - expense))
                    WalletState.objects.create(wallet=key,
                        amount=state.amount + Decimal(str(income - expense)),
                        moment=begin + RD(months=+1))
