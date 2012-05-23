# -*- coding: utf-8 -*-

from functools import wraps

from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.utils.hashcompat import sha_constructor


def cache_factory(key_tpl, timeout):
    u"""
    Возвращает декоратор кэширования.

    @type  key_tpl: unicode
    @param key_tpl: Шаблон ключа для размещения в кэше.
    @type  timeout: integer
    @param timeout: Время кэширования в секундах.

    @rtype: callable
    @return: Декоратор кэширования.
    """
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):

            def _params_to_hash(*a, **k):
                return reduce(lambda x, y: x + y,
                    map(unicode, list(a) + k.values()))

            key_raw = key_tpl % _params_to_hash(*args, **kwargs)
            key = sha_constructor(key_raw.encode('utf-8')).hexdigest()
            value = cache.get(key)
            if value is None:
                value = func(*args, **kwargs)
                cache.set(key, value, timeout)
            return value
        return wrapped
    decorator = method_decorator(decorator)
    return decorator
