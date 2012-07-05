# -*- coding: utf-8 -*-

from django import forms


class ImageOptsForm(forms.Form):
    up = forms.BooleanField(required=False)
    base64 = forms.BooleanField(required=False)

    def clean(self):
        pass