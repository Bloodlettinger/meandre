# -*- coding: utf-8 -*-

from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile

from . import render_to_json
from . import forms


@csrf_exempt
@render_to_json()
def image(request):
    form = forms.ImageOptsForm(request.GET or None)
    if form.is_valid():
        pass
    #import pdb; pdb.set_trace()
    return dict()