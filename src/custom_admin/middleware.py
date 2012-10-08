# -*- coding: utf-8 -*-

import re

from django.shortcuts import redirect

PREF_VAR = 'ADMIN_PER_USER_PREF'
ORDER_VAR = 'o'
FILTER_TAIL = '__exact'
CUSTOM_FILTERS = ('status', )
PATH = '/admin/storage/'
EXCLUDE_RE = re.compile(r'(\d+|add)\/$')
CHANGE_URL_RE = re.compile(r'.*\/\d+\/$')


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
            current_path = request.META.get('PATH_INFO')
            http_referer = request.META.get('HTTP_REFERER')
            if 0 == len(request.GET) and http_referer:
                if current_path not in http_referer \
                    or current_path in http_referer and CHANGE_URL_RE.search(http_referer):
                    # пришли из другого раздела админки
                    # или возвратились со страницы редактирования модели
                    if 0 < len(opts):
                        # выполняем перенаправление
                        return redirect(u'%s?%s' % (
                            request.path,
                            '&'.join(map(lambda x: '%s=%s' % x, opts.items())))
                        )
                else:
                    # удаление элементов, отсутствующих в запросе
                    for key in list(set(opts.keys()) - set(request.GET.keys())):
                        del(opts[key])
                    # сохраняем состояние
                    prefs[request.path] = opts
                    request.session[PREF_VAR] = prefs
            else:
                # сортировка
                if ORDER_VAR in request.GET:
                    opts[ORDER_VAR] = request.GET[ORDER_VAR]
                # фильтрация: добавляем/обновляем фильтры, а затем убираем старые
                for key in filter(lambda x: x.endswith(FILTER_TAIL), request.GET):
                    opts[key] = request.GET[key]
                for key in CUSTOM_FILTERS:
                    value = request.GET.get(key)
                    if value is not None:
                        opts[key] = value

                if http_referer and current_path in http_referer:
                    # удаление элементов, отсутствующих в запросе
                    for key in list(set(opts.keys()) - set(request.GET.keys())):
                        del(opts[key])

                # сохраняем состояние
                prefs[request.path] = opts
                request.session[PREF_VAR] = prefs
