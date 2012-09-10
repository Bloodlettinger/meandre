# -*- coding: utf-8 -*-

from django.http import HttpResponse

from . import models


def get_customer_code(request):
    action = request.GET.get('action')
    if 'hc' == action:
        lowest = True
    elif 'hm' == action:
        lowest = False
    else:
        return HttpResponse('fail')
    code = models.Customer.generate_code(lowest=lowest)
    return HttpResponse('{0:04}'.format(code))
