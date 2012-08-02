# -*- coding: utf-8 -*-

from fab_deploy import *
from . import local_settings as settings

COMMON_OPTIONS = dict(
    DB_USER=settings.DB_USER,
    )


@define_host(settings.SERVER_URL)
def production():
    options = COMMON_OPTIONS.copy()
    return options
