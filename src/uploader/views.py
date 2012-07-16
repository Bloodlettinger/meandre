# -*- coding: utf-8 -*-

import os
import logging
import StringIO as StringIO
from PIL import Image
from datetime import datetime

from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse

from . import forms
from . import models

logger = logging.getLogger(u'uploader')


@login_required
@csrf_exempt
def image(request):
    form = forms.ImageOptsForm(request.GET or None)

    if not form.is_valid():
        logger.error(u'Form ImageOptsForm is not valid!')
        raise Http404

    data = request.body
    if u'true' == form.cleaned_data.get('base64'):
        try:
            data = data.decode('base64')
        except Exception, e:
            logger.error(u'%s: %s' % (e, data))
            raise Http404

    file_data = ContentFile(data)
    file_name = request.META.get('HTTP_UP_FILENAME', 'unknown').decode('utf-8')
    file_size = request.META.get('HTTP_UP_SIZE', 0).decode('utf-8')
    file_type = request.META.get('HTTP_UP_TYPE', 'text/plain').decode('utf-8')

    save_model = True
    obj = models.Queue(
        uploaded_by=request.user,
        file_name=file_name,
        file_size=file_size,
        file_type=file_type
        )
    obj.tags = form.cleaned_data.get('tags')
    obj.image.save(file_name, file_data, save=save_model)

    context = dict(obj=obj)
    return TemplateResponse(request, 'uploader/frame.html', context)


@login_required
@csrf_exempt
def done(request):
    form = forms.DoneForm(request.POST or None)
    if not form.is_valid():
        logger.error(u'Form DoneForm is not valid!')
        raise Http404

    params = form.cleaned_data

    pk = params.get('image')
    try:
        obj = models.Queue.objects.get(pk=pk)
    except models.Queue.DoesNotExist:
        logger.error(u'Unknown image %i in Queue!' % pk)
        raise Http404

    if params.get('is_cropped'):
        img = Image.open(obj.image)
        orig_width, orig_height = img.size
        shown_width = params.get('shown_width')
        shown_height = params.get('shown_height')
        crop_x = params.get('point_x')
        crop_y = params.get('point_y')
        crop_w = params.get('width')
        crop_h = params.get('height')
        ratio_horizontal = float(orig_width) / float(shown_width)
        ratio_vertical = float(orig_height) / float(shown_height)

        x1 = crop_x * ratio_horizontal
        y1 = crop_y * ratio_vertical
        x2 = (crop_x + crop_w) * ratio_horizontal
        y2 = (crop_y + crop_h) * ratio_vertical

        box = map(int, (x1, y1, x2, y2))
        region = img.crop(box)
        region_io = StringIO.StringIO()
        region.save(region_io, format='PNG')

        obj.file_name = u'%s.png' % os.path.splitext(obj.file_name)[0]
        obj.file_type = 'image/png'
        obj.file_size = region_io.len

        file_data = InMemoryUploadedFile(region_io, None,
            obj.file_name, obj.file_type, obj.file_size, None)

        save_model = False
        obj.image.save(obj.file_name, file_data, save=save_model)

    obj.confirmed_by = request.user
    obj.confirmed_at = datetime.now()
    obj.save()

    context = dict(obj=obj)
    return TemplateResponse(request, 'uploader/frame.html', context)
