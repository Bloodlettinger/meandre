# -*- coding: utf-8 -*-

from django.contrib import messages
from django.views.generic.simple import direct_to_template


def index(request):
    context = dict()
    return direct_to_template(request, 'frontend/index.html', context)
