# -*- coding: utf-8 -*-

from django import template
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

register = template.Library()


TAX_PFR = 0.336
TAX_NDFL = 0.13
K_BASE = 0.1
ACCOUNT_TYPE = 1
K_ADD = 1.1 * ACCOUNT_TYPE
K_ZAP = K_ADD * (1 + K_BASE)


@register.inclusion_tag('phases/report_block.html')
def phase_area(phase):
    steps = []
    for step in phase.step_set.all():
        item = step.relation_set.all()[0]

        dur_a = item.duration_a
        dur_b = item.duration_b
        cost = item.cost
        STAFF = cost == 0

        price = (dur_a + dur_b) * step.price * step.times if STAFF else cost
        pfr = price * TAX_PFR
        ndfl = price * TAX_NDFL

        price_tax = (price + pfr + ndfl) * (1.2 if STAFF else 1)
        price_zap = price_tax * K_ZAP if STAFF else cost

        steps.append((step.title, step.price, step.times, dur_a, dur_b,
            cost, price, pfr, ndfl, price_tax, price_zap))

        total = dict()
        for step in steps:
            for index in (1,3,4,5,6,7,8,9,10):
                value = total.get(index, 0)
                value += step[index]
                total[index] = value
        total = (
            mark_safe(_(u'Total')),
            total[1],
            mark_safe('&nbsp;'),
            total[3],
            total[4],
            total[5],
            total[6],
            total[7],
            total[8],
            total[9],
            total[10],
        )
    return dict(
        pk=phase.pk,
        title=phase.title,
        headers=(
            _(u'Ставка'), _(u'K'), _(u'Hours, A'), _(u'Hours, B'), _(u'Cost'),
            _(u'Price'), _(u'Tax, PFR'), _(u'Tax, NDFL'), _(u'Price with Taxes'),
            _(u'С запасом'),
            ),
        steps=steps,
        total=total,
    )
