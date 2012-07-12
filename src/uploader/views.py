# -*- coding: utf-8 -*-

import logging

from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse

from . import forms
from . import models
from .import render_to_json

logger = logging.getLogger(u'uploader')


@login_required
@csrf_exempt
def image(request):
    form = forms.ImageOptsForm(request.GET or None)

    if not form.is_valid():
        logger.error(u'Form is not valid!')
        return u'error'

    data = request.body
    if u'true' == form.cleaned_data.get('base64'):
        try:
            data = data.decode('base64')
        except Exception, e:
            logger.error(u'%s: %s' % (e, data))
            return u'error'

    file_data = ContentFile(data)
    file_name = request.META.get('HTTP_UP_FILENAME', 'unknown').decode('utf-8')
    file_size = request.META.get('HTTP_UP_SIZE', 0).decode('utf-8')
    file_type = request.META.get('HTTP_UP_TYPE', 'text/plain').decode('utf-8')

    save_model = True
    obj = models.Queue(
        user=request.user,
        file_name=file_name,
        file_size=file_size,
        file_type=file_type
        )
    obj.image.save(file_name, file_data, save=save_model)

    context = dict(obj=obj)
    return TemplateResponse(request, 'uploader/frame.html', context)


@login_required
@csrf_exempt
@render_to_json()
def done(request):
    form = forms.DoneForm(request.POST or None)
    if form.is_valid():
        print form.cleaned_data
    return dict(status=u'ok')
