# -*- coding: utf-8 -*-

import logging

from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required

from . import render_to_json
from . import forms
from . import models

logger = logging.getLogger(u'uploader')


@login_required
@csrf_exempt
@render_to_json()
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
    file_name = request.META.get('HTTP_UP_FILENAME', 'unknown')
    file_size = request.META.get('HTTP_UP_SIZE', 0)
    file_type = request.META.get('HTTP_UP_TYPE', 'text/plain')

    save_model = True
    obj = models.Queue(
        user=request.user,
        file_name=file_name,
        file_size=file_size,
        file_type=file_type
        )
    obj.image.save(file_name, file_data, save=save_model)
    return u'ok'
