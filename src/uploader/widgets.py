# -*- coding: utf-8 -*-

from django import forms
from django.utils.safestring import mark_safe
from django.contrib.admin.templatetags.admin_static import static


class StateWidget(forms.widgets.CheckboxInput):

    class Media:
        css = dict(all=(static('uploader/css/widgets/states.css'), ))

    def render(self, name, value, attrs=None):
        value = super(StateWidget, self).render(name, value, attrs)
        tpl = """
        <span class="state-%(state)s">
            %(input)s
            <i class="icon-%(state)s"></i>
        </span>
        """
        context = dict(state=name, input=value)
        return mark_safe(tpl % context)
