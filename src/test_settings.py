# -*- coding: utf-8 -*-

from settings import *

del(DATABASES['default2'])
del(DATABASES['legacy'])


class Test(object):
    ADMIN_LOGIN = 'admin'
    ADMIN_PASS = 'q1'
    ADMIN_EMAIL = 'admin@this.ru'
