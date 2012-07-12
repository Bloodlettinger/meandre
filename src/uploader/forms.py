# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from ..storage.models import Project


class ImageOptsForm(forms.Form):
    up = forms.CharField(max_length=5, required=False)
    base64 = forms.CharField(max_length=5, required=False)


class DoneForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.all(), empty_label=_(u'Choose a Project'))
    image = forms.IntegerField(widget=forms.HiddenInput)
    is_cropped = forms.BooleanField(required=False, widget=forms.HiddenInput)
    point_x = forms.IntegerField(required=False, widget=forms.HiddenInput)
    point_y = forms.IntegerField(required=False, widget=forms.HiddenInput)
    width = forms.IntegerField(required=False, widget=forms.HiddenInput)
    height = forms.IntegerField(required=False, widget=forms.HiddenInput)
