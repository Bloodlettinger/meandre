# -*- coding: utf-8 -*-

from django import forms


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
