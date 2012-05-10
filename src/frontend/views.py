# -*- coding: utf-8 -*-

from django.contrib import messages
from django.views.generic.simple import direct_to_template

from src.storage import models


def index(request):
    context = dict(
        clients=models.Customer.objects.filter(logo__isnull=False, url__isnull=False),
        recommendations=models.Recommendation.objects.all()
    )
    return direct_to_template(request, 'frontend/index.html', context)
