# -*- coding: utf-8 -*-

import itertools
import operator
from datetime import datetime, date

from django.db import models
from django.db.models.query import QuerySet

from model_utils.managers import PassThroughManager
from tagging.models import Tag

from . decorators import cache_factory
from . exceptions import WalletStateNotFound


class WalletStateManager(models.Manager):

    def last(self, wallet_type):
        try:
            return self.filter(wallet=wallet_type).order_by('-moment')[0]
        except IndexError:
            raise WalletStateNotFound

    def history(self):
        return self.values('moment').annotate(models.Sum('amount'))


class FinanceTransactionManager(models.Manager):

    def wallets(self):
        u"""Возвращает состояние всех аккаунтов в виде словаря."""
        from . models import WALLET_TYPE
        return [(title, self.wallet_state(key))\
            for key, title in WALLET_TYPE]

    @cache_factory('wallet_%s', 60 * 60)
    def wallet_state(self, wallet_type, timepoint=None):
        u"""Возвращает состояние указанного аккаунта."""
        amount = 0.0
        try:
            from . models import WalletState
            state = WalletState.objects.last(wallet_type)
        except WalletStateNotFound:
            qs = self.filter(wallet=wallet_type)
        else:
            amount = state.amount
            qs = self.filter(wallet=wallet_type, done_at__gt=state.moment)

        if isinstance(timepoint, (datetime, date)):
            qs = qs.filter(done_at__lt=timepoint)

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
        return self.filter(is_public=True,
            code__in=map(lambda x: x.name, Tag.objects.all())  # т.е. есть изображения
            )

    def for_stats(self):
        return self.filter(in_stats=True)

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
        total = self.model.objects.count()

        return dict(
            year_A=A,
            year_B=B,
            total_A=total_A,
            total_B=total_B,
            total=total,
        )

    def total_values(self, year=None):
        winned = self.model.objects.winned(year)
        if year is None:
            total = self.all()
        else:
            total = self.filter(begin__year=year)
        res = dict(
            total=total.count(),
            winned=winned.count(),
            dist=self.distribution(winned)
        )
        res.update(winned.aggregate(
            square=models.Sum('object_square'),
            production=models.Sum('duration_production'),
            change=models.Sum('duration_changes'),
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

    def directions(self):
        qs = self.model.objects.winned().exclude(in_stats=False)
        total = qs.count()
        qs = qs.values('ptype')
        qs = qs.annotate(count=models.Count('ptype'), meters=models.Sum('object_square'))
        qs = qs.values_list('ptype', 'count', 'meters')
        data = dict((key, (count, meters)) \
            for key, count, meters in sorted(qs, key=lambda x: x[0]))

        return dict(
            work=dict(
                percent=data[1][0] * 100 / total,
                count=data[1][0],
                meters=data[1][1]),
            home=dict(
                percent=data[2][0] * 100 / total,
                count=data[2][0],
                meters=data[2][1]),
            shop=dict(
                percent=data[3][0] * 100 / total,
                count=data[3][0],
                meters=data[3][1]),
            ent=dict(
                percent=data[4][0] * 100 / total,
                count=data[4][0],
                meters=data[4][1]),
            )
