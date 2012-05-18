# -*- coding: utf-8 -*-
from django import forms

from . import models


class CustomUserForm(forms.ModelForm):

    class Meta:
        model = models.CustomUser
