# -*- coding: utf-8 -*-

from django import forms


class ImageOptsForm(forms.Form):
    up = forms.CharField(max_length=5, required=False)
    base64 = forms.CharField(max_length=5, required=False)
