# -*- coding: utf-8 -*-

from functools import wraps

from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.utils.hashcompat import sha_constructor


def cache_factory(key_tpl, timeout):
    def decorator(func):
        @wraps(func)
        def wrapped(wallet_type):
            key_raw = key_tpl % wallet_type
            key = sha_constructor(key_raw.encode('utf-8')).hexdigest()
            value = cache.get(key)
            if value is None:
                value = func(wallet_type)
                cache.set(key, value, timeout)
            return value
        return wrapped
    decorator = method_decorator(decorator)
    return decorator
