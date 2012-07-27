# -*- coding: utf-8 -*-

from django import forms
from django.forms.models import modelformset_factory

from ..uploader.models import Queue as ImageQueue

from . import models

ImagePositionFormSet = modelformset_factory(ImageQueue, fields=('id', 'position', ), extra=0)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        # поле кода проекта разрешено редактировать только для существующих
        # проектов с незаполненным кодом
        if not (self.instance and self.instance.pk and self.instance.code is None):
            self.fields['code'].widget = forms.HiddenInput()

    def clean_code(self):
        if not (self.instance and self.instance.pk and self.instance.code is None):
            return self.instance.code
        else:
            return self.cleaned_data['code']
