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

    def clean(self):
        cleaned_data = super(ProjectForm, self).clean()

        created_at = cleaned_data.get('reg_date')
        begin_at = cleaned_data.get('begin')
        end_at = cleaned_data.get('end')
        finished_at = cleaned_data.get('finished_at')

        if created_at and begin_at and created_at > begin_at:
            self._errors['begin'] = self.error_class([
                _('The value is lower than a value of `Registered` field.')])
            del cleaned_data['begin']

        if begin_at and end_at and begin_at > end_at:
            self._errors['end'] = self.error_class([
                _('The value is lower than a value of `Begin` field.')])
            del cleaned_data['end']

        if end_at and finished_at and end_at > finished_at:
            self._errors['end'] = self.error_class([
                _('The value is greater than a value of `Finished` field.')])

        return cleaned_data
