# -*- coding: utf-8 -*-

from . import settings as _settings


def settings(request):
    return dict(settings=_settings)
