# -*- coding: utf-8 -*-

from datetime import date, datetime


def ddmmyy(value):
    if isinstance(value, (date, datetime)):
        return value.strftime('%d.%m.%y')
    else:
        return u'--'
