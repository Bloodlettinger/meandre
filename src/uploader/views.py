# -*- coding: utf-8 -*-

import os
import logging
import StringIO as StringIO
from PIL import Image
from datetime import datetime

from django.http import Http404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404

from . import settings
from . import forms
from . import models
from . import render_to_json

logger = logging.getLogger(u'uploader')


class HttpResponseDeleted(HttpResponse):
    status_code = 204


class HttpResponseNotImplemented(HttpResponse):
    status_code = 501


@login_required
@csrf_exempt
def image_upload(request, template='uploader/frame_inline.html'):
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

    user_agent = request.META.get('HTTP_USER_AGENT').lower()
    if 0 <= user_agent.find('firefox'):
        post_form = forms.UploadAsFileForm(request.POST, request.FILES)
        if not post_form.is_valid():
            logger.error(u'Form UploadAsFileForm is not valid!')
            raise Http404
        else:
            file_data = request.FILES.get('upload')
            file_name = file_data.name
    elif 0 <= user_agent.find('chrome'):
        file_data = ContentFile(data)
        file_name = request.META.get('HTTP_UP_FILENAME', 'unknown').decode('utf-8')
    else:
        raise HttpResponseNotImplemented

    # все изображения конвертируются в PNG
    data = Image.open(file_data)
    io = StringIO.StringIO()
    data.save(io, format='PNG')

    file_name = u'%s.png' % os.path.splitext(file_name)[0]
    file_type = 'image/png'
    file_size = io.len

    file_data = InMemoryUploadedFile(
        io, None, file_name, file_type, file_size, None)

    save_model = True
    obj = models.Queue(
        uploaded_by=request.user,
        file_name=file_name,
        file_size=file_size,
        file_type=file_type
        )
    obj.tags = form.cleaned_data.get('tags')
    obj.position = form.cleaned_data.get('position')
    obj.image.save(file_name, file_data, save=save_model)

    context = dict(
        obj=obj,
        prefix='images_set',
        counter=form.cleaned_data.get('position')
        )
    return TemplateResponse(request, template, context)


@login_required
@csrf_exempt
def image_change(request, template='uploader/frame_inline.html'):
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

    if 'delete' in request.POST:
        obj.delete()  # the file itself will be deleted with post_delete signal
        return HttpResponseDeleted()

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
        dim = (settings.UPLOADER_IMAGE_MAX_WIDTH, settings.UPLOADER_IMAGE_MAX_HEIGHT)
        region = img.crop(box).resize(dim, Image.ANTIALIAS)
        region_io = StringIO.StringIO()
        region.save(region_io, format='PNG')

        # удаляем оригинал
        obj.image.delete(save=False)

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
    return TemplateResponse(request, template, context)


@login_required
@render_to_json()
def image_state(request, pk=None, template='uploader/frame_inline.html'):
    tags = get_object_or_404(models.Queue, pk=pk).tags
    return dict(
        visible='visible' in tags,
        staff='staff' in tags,
        teaser='teaser' in tags
        )
