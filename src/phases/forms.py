# -*- coding: utf-8 -*-

from django import forms
from django.forms.models import modelformset_factory

from . import models


class PhaseForm(forms.ModelForm):
    class Meta:
        model = models.Relation
        fields = ('step', 'duration_a', 'duration_b', 'cost')

    def __init__(self, *args, **kwargs):
        super(PhaseForm, self).__init__(*args, **kwargs)
        self.fields['step'].widget.attrs['readonly'] = True

PhasesFormSet = modelformset_factory(models.Relation, form=PhaseForm, extra=0)
