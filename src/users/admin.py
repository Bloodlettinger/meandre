# -*- coding: utf-8 -*-
u"""
Модуль представления моделей на интерфейсе администратора.
"""

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

from . import models
from . import forms


class CustomGroup(GroupAdmin):
    u"""
    Класс представления модели L{CustomGroup<users.models.CustomGroup>}.
    """
    pass

admin.site.unregister(Group)
admin.site.register(models.CustomGroup, CustomGroup)


class CustomUser(UserAdmin):
    u"""
    Класс представления модели L{CustomUser<users.models.CustomUser>}.
    """
    form = forms.CustomUserForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Profile'), {'fields': ('phone', 'birth_date', 'sex')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Groups'), {'fields': ('groups',)}),
    )

admin.site.unregister(User)
admin.site.register(models.CustomUser, CustomUser)
