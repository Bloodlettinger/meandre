# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from . import widgets


class ImageOptsForm(forms.Form):
    base64 = forms.CharField(max_length=5, required=False)
    tags = forms.CharField(max_length=255, required=False)
    position = forms.IntegerField(required=False)


class UploadAsFileForm(forms.Form):
    upload = forms.ImageField()


class DoneForm(forms.Form):
    image = forms.IntegerField(widget=forms.HiddenInput)
    shown_width = forms.IntegerField(widget=forms.HiddenInput)
    shown_height = forms.IntegerField(widget=forms.HiddenInput)
    is_cropped = forms.BooleanField(required=False, widget=forms.HiddenInput)
    point_x = forms.FloatField(required=False, widget=forms.HiddenInput)
    point_y = forms.FloatField(required=False, widget=forms.HiddenInput)
    width = forms.IntegerField(required=False, widget=forms.HiddenInput)
    height = forms.IntegerField(required=False, widget=forms.HiddenInput)

    visible = forms.BooleanField(required=False, label=u'', widget=widgets.StateWidget(
        attrs=dict(title=_(u'Make this image visible for ordinary users.'))))
    staff = forms.BooleanField(required=False, label=u'', widget=widgets.StateWidget(
        attrs=dict(title=_(u'Make this image visible for staff only.'))))
    teaser = forms.BooleanField(required=False, label=u'', widget=widgets.StateWidget(
        attrs=dict(title=_(u'Use this image for teaser.'))))
