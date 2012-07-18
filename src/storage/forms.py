# -*- coding: utf-8 -*-

from django import forms
from django.forms.models import inlineformset_factory
from django.forms.models import modelformset_factory
from django.utils.translation import ugettext_lazy as _

from ..uploader.models import Queue as ImageQueue

from . import models


def project_inline_formset_clean(self):
    is_teaser_used = False
    is_pro6_used = False
    for i in range(0, self.total_form_count()):
        form = self.forms[i]
        if form.cleaned_data.get('is_teaser'):
            if not is_teaser_used:
                is_teaser_used = True
            else:
                raise forms.ValidationError(_(u'Only one image may be choosen as teaser!'))
        if form.cleaned_data.get('is_pro6'):
            if not is_pro6_used:
                is_pro6_used = True
            else:
                raise forms.ValidationError(_(u'Only one image may be choosen for pro6 module!'))


ProjectImageInlineFormset = inlineformset_factory(models.Project, models.ProjectImage)
ProjectImageInlineFormset.clean = project_inline_formset_clean

ImagePositionFormSet = modelformset_factory(ImageQueue, fields=('id', 'position', ))
