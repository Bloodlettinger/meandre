# -*- coding: utf-8 -*-

PREF_VAR = 'ADMIN_PER_USER_PREF'
ORDER_VAR = 'o'
CLEAR_VAR = 'PREF_CLEAR'


class ChangelistPreferencesMiddleware(object):
    u"""
    Мидлварь обеспечивает сохранение сортировки по полям моделей
    в админке для каждого пользователя.
    """

    def process_request(self, request):
        if request.path.startswith('/admin/storage/'):
            prefs = request.session.get(PREF_VAR, dict())
            opts = prefs.get(request.path, dict())

            if ORDER_VAR in request.GET:
                opts[ORDER_VAR] = request.GET[ORDER_VAR]
            else:
                ordering = opts.get(ORDER_VAR)
                if ordering:
                    GET = dict(request.GET)
                    GET.update({ORDER_VAR: ordering})
                    request.GET = GET

            prefs.update({request.path: opts})
            request.session[PREF_VAR] = prefs
