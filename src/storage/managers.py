# -*- coding: utf-8 -*-

import operator

from django.db import models
from django.db.models.query import QuerySet

from model_utils.managers import PassThroughManager

from . decorators import cache_factory
from . exceptions import WalletStateNotFound


class WalletStateManager(models.Manager):

    def last(self, wallet_type):
        try:
            return self.filter(wallet=wallet_type).order_by('-end')[0]
        except IndexError:
            raise WalletStateNotFound


class FinanceTransactionManager(models.Manager):

    @cache_factory('wallet_%s', 60 * 60)
    def wallet_state(self, wallet_type):
        amount = 0.0
        try:
            from . models import WalletState
            state = WalletState.objects.last(wallet_type)
        except WalletStateNotFound:
            qs = self.filter(wallet=wallet_type)
        else:
            amount = state.amount
            qs = self.filter(wallet=wallet_type, done_at__gt=state.end)

        ops = {1: operator.add, 2: operator.sub}

        for item in qs:
            action = ops.get(item.transaction_type)
            amount = action(amount, item.amount)
        return amount


class ProjectQuerySet(QuerySet):

    def winned(self):
        WINNED = 2
        return self.filter(status=WINNED)

    def public(self):
        return self.filter(is_public=True)

    def active(self):
        return self.filter(is_active=True)


class ProjectManager(PassThroughManager):
    use_for_related_fields = True

    def __init__(self):
        super(ProjectManager, self).__init__(ProjectQuerySet)
