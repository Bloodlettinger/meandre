# -*- coding: utf-8 -*-

from django.forms.models import modelformset_factory

from ..uploader.models import Queue as ImageQueue


ImagePositionFormSet = modelformset_factory(ImageQueue, fields=('id', 'position', ), extra=0)
