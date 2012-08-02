# -*- coding: utf-8 -*-

from django import forms
from django.forms.models import modelformset_factory
from django.utils.translation import ugettext_lazy as _

from ..uploader.models import Queue as ImageQueue

from . import models

ImagePositionFormSet = modelformset_factory(ImageQueue, fields=('id', 'position', ), extra=0)


class ProjectForm(forms.ModelForm):
    u""" Форма необходима для решения #91. """
    class Meta:
        model = models.Project

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        # поле кода проекта разрешено редактировать только для существующих
        # проектов с незаполненным кодом
        if self.instance and self.instance.pk:
            self.fields['code'].widget = forms.widgets.TextInput(attrs=dict(readonly='readonly'))
            self.fields['customer'].help_text = _(u'This value is immutable for an existing project.')
        else:
            self.fields['code'].required = False

    def clean_code(self):
        if self.instance and self.instance.pk:
            return self.instance.code
        else:
            return self.cleaned_data['code']

    def clean_customer(self):
        if self.instance and self.instance.pk:
            return self.instance.customer
        else:
            return self.cleaned_data['customer']
