# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import login as original_login
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse


def login(request):
    u"""
    Вызывает соответствующее представление Django, анализирует результат.
    В случае ошибки генерирует сообщение и возвращает пользователя на прежнюю страницу.
    """
    response = original_login(request)
    if isinstance(response, HttpResponseRedirect):
        return response
    else:
        messages.error(request, _(u'Your credentials are wrong. Sorry.'))
        return_to = request.REQUEST.get(REDIRECT_FIELD_NAME, reverse('frontend:index'))
        return HttpResponseRedirect(return_to)
