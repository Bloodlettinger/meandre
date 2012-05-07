# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.db.models.signals import post_save
from django.contrib.auth.models import User

from .models import CustomUser


def create_profile(sender, instance, created, **kwargs):
    u"""
    При создании пользователя через базовую модель, автоматом создаём
    для него профиль. Пользователи без профиля в админке не видны.
    """
    if created:
        values = {}
        for field in sender._meta.local_fields:
            values[field.attname] = getattr(instance, field.attname)
        user = CustomUser(**values)
        user.save()
post_save.connect(create_profile, User)
