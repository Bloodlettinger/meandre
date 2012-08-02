# -*- coding: utf-8 -*-

from functools import wraps

from fabric import api

from . hosts import production

ENV_DIR = 'site1/env'


def virtualenv():
    return api.prefix('source %s/bin/activate' % ENV_DIR)


def inside_virtualenv(func):
    @wraps(func)
    def inner(*args, **kwargs):
        with virtualenv():
            return func(*args, **kwargs)
    return inner


@inside_virtualenv
def touch_server():
    api.run('touch ~/www/site1/webapp/webapp.wsgi', shell=False)

production()
