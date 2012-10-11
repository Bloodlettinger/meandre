# -*- coding: utf-8 -*-

from functools import wraps
from django.utils.safestring import mark_safe


def description(value):
    def decorator(func):
        func.short_description = value
        return func
    return decorator

def order_hint(field):
    def decorator(func):
        func.admin_order_field = field
        return func
    return decorator

def allow_tags(func):
    @wraps(func)
    def inner(*args, **kwargs):
        return mark_safe(func(*args, **kwargs))
    inner.allow_tags = True
    return inner

def boolean(func):
    func.boolean = True
    return func
