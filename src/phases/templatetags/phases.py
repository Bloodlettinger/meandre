# -*- coding: utf-8 -*-

from django import template
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from .. import TAX_PFR, TAX_NDFL, K_ZAP

register = template.Library()


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

        steps.append(
            [(step.title, 'left', 'text'),
             (step.price, 'right', 'int'),
             (step.times, 'right', 'float'),
             (dur_a, 'right', 'int'),
             (dur_b, 'right', 'int'),
             (cost, 'right', 'int'),
             (price, 'right', 'float'),
             (pfr, 'right', 'float'),
             (ndfl, 'right', 'float'),
             (price_tax, 'right', 'float'),
             (price_zap, 'right', 'float'),
             ])

        total = dict()
        for step in steps:
            for index in (1,3,4,5,6,7,8,9,10):
                value = total.get(index, 0)
                value += step[index][0]
                total[index] = value
        total = (
            [(mark_safe(_(u'Total')), 'left', 'text'),
             (total[1], 'right', 'int'),
             (mark_safe('&nbsp;'), 'right', 'text'),
             (total[3], 'right', 'int'),
             (total[4], 'right', 'int'),
             (total[5], 'right', 'int'),
             (total[6], 'right', 'float'),
             (total[7], 'right', 'float'),
             (total[8], 'right', 'float'),
             (total[9], 'right', 'float'),
             (total[10], 'right', 'float'),
             ])
    return dict(
        pk=phase.pk,
        title=phase.title,
        headers=(
            _(u'Rate'), _(u'K'), _(u'Hours, A'), _(u'Hours, B'), _(u'Cost'),
            _(u'Price'), _(u'Tax, PFR'), _(u'Tax, NDFL'), _(u'Price with Taxes'),
            _(u'incl. Reserve'),
            ),
        steps=steps,
        total=total,
    )
