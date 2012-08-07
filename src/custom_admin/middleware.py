# -*- coding: utf-8 -*-

import re

from django.shortcuts import redirect

PREF_VAR = 'ADMIN_PER_USER_PREF'
ORDER_VAR = 'o'
FILTER_TAIL = '__exact'
PATH = '/admin/storage/'
EXCLUDE_RE = re.compile(r'(\d+|add)\/$')


class ChangelistPreferencesMiddleware(object):
    u"""
    Мидлварь обеспечивает сохранение параметров сортировки и фильтрации
    по полям моделей в админке для каждого пользователя.

    Если GET пуст, значит добавляем туда опции из сессии пользователя.

    Иначе, сохраняем параметры сортировки и фильтрации в сессии пользователя.
    """

    def process_request(self, request):
        if request.method == 'GET' \
            and request.path.startswith(PATH) \
            and not EXCLUDE_RE.search(request.path):

            prefs = request.session.get(PREF_VAR, dict())
            opts = prefs.get(request.path, dict())

            if 0 < len(request.GET):
                # сортировка
                if ORDER_VAR in request.GET:
                    opts[ORDER_VAR] = request.GET[ORDER_VAR]
                # фильтрация
                for key in filter(lambda x: x.endswith(FILTER_TAIL), request.GET):
                    opts[key] = request.GET[key]
                # сохраняем состояние
                prefs[request.path] = opts
                request.session[PREF_VAR] = prefs
            else:
                if 0 < len(opts):
                    # выполняем перенаправление
                    return redirect(u'%s?%s' % (
                        request.path,
                        '&'.join(map(lambda x: '%s=%s' % x, opts.items())))
                    )
