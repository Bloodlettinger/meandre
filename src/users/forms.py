# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django import forms

from . import models


class CustomUserForm(forms.ModelForm):

    class Meta:
        model = models.CustomUser
