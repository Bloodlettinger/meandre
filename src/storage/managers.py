# -*- coding: utf-8 -*-

import itertools
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

    def winned(self, year=None):
        WINNED = 2
        qs = self.filter(status=WINNED)
        if year is not None:
            qs = qs.filter(begin__year=year)
        return qs

    def public(self):
        return self.filter(is_public=True)

    def active(self):
        return self.filter(is_active=True)

    def get_neighbour(self, obj, next=True):
        default = dict(slug__isnull=False, customer__logo__isnull=False, is_public=True)
        if next:
            direction, params = 'pk', dict(default, pk__gt=obj.pk)
        else:
            direction, params = '-pk', dict(default, pk__lt=obj.pk)
        try:
            return self.order_by(direction).filter(**params)[0]
        except IndexError:
            return None

    def get_next(self, obj):
        return self.get_neighbour(obj, next=True)

    def get_prev(self, obj):
        return self.get_neighbour(obj, next=False)


class ProjectManager(PassThroughManager):
    use_for_related_fields = True

    def __init__(self):
        super(ProjectManager, self).__init__(ProjectQuerySet)


class ProjectStatisticManager(models.Manager):

    # CACHE IT
    def compare_years(self, A, B):
        total_A = self.total_values(year=A)
        total_B = self.total_values(year=B)

        return dict(
            year_A=A,
            year_B=B,
            total_A=total_A,
            total_B=total_B,
        )

    def total_values(self, year=None):
        winned = self.model.objects.winned(year)
        res = dict(
            total=self.all().count(),
            winned=winned.count(),
            dist=self.distribution(winned)
        )
        res.update(winned.aggregate(
            square=models.Sum('object_square'),
            production=models.Sum('duration_production'),
            change=models.Sum('duration_changes'),
            discuss=models.Sum('duration_discussion'),
            other=models.Sum('duration_other'),
            price=models.Sum('price_full'),
            ))
        res['speed'] = res['square'] / res['production']
        res['customers'] = self.customer_types(year)
        return res

    def distribution(self, qs):
        res = qs.values('ptype').annotate(
            count=models.Count('ptype'),
            price=models.Sum('price_full'),
            square=models.Sum('object_square'),
            price_avg=models.Sum('price_average')
            )

        def _handler(item):
            try:
                item['price_avg'] = item['price'] / item['square']
            except ZeroDivisionError:
                item['price_avg'] = 0.0
            return item

        # izip_longest реализует функционал zip() для длинных списков,
        # но итерация идёт по самому длинному, в пустые места вставляется
        # значение параметра fillvalue
        # первый параметр - это отсортированный список возможных идентификаторов
        # второй параметр - список типов проектов, отсортированный по типу
        out = {}
        for a, b in itertools.izip_longest(
            map(lambda x: int(x[0]),
                self.order_by('ptype').values_list('ptype').distinct()),
            sorted(res, key=lambda x: x['ptype']),
            fillvalue=dict(count=0, price=0.0, square=0.0)):

            try:
                b['price_avg'] = b['price'] / b['square']
            except ZeroDivisionError:
                b['price_avg'] = 0.0

            out[a] = b

        return out

    def customer_types(self, year=None):
        qs = self.model.objects.winned(year)
        qs = qs.values_list('customer__customer_type')
        res = qs.annotate(count=models.Count('customer__customer_type'))
        return dict((a, b) for a, b in sorted(res, key=lambda x: x[0]))
