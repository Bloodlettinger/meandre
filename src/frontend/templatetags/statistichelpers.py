# -*- coding: utf-8 -*-

from django.utils import formats
from django import template
from django.utils.translation import ugettext, ungettext


register = template.Library()


@register.filter(is_safe=True)
def moneyformat(value):
    try:
        value = float(value)
    except (TypeError, ValueError, UnicodeDecodeError):
        return ungettext("%(size)d", "%(size)d", 0) % {'size': 0}

    _format = lambda value: formats.number_format(round(value, 1), 1)

    if value < 1024:
        return ungettext("%(size)d", "%(size)d", 0) % {'size': value}
    if value < 1024 * 1024:
        return ugettext("%s K") % _format(value / 1024)
    if value < 1024 * 1024 * 1024:
        return ugettext("%s M") % _format(value / (1024 * 1024))
    if value < 1024 * 1024 * 1024 * 1024:
        return ugettext("%s G") % _format(value / (1024 * 1024 * 1024))
    if value < 1024 * 1024 * 1024 * 1024 * 1024:
        return ugettext("%s T") % _format(value / (1024 * 1024 * 1024 * 1024))
    return ugettext("%s P") % _format(value / (1024 * 1024 * 1024 * 1024 * 1024))
