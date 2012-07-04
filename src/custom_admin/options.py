# -*- coding: utf-8 -*-

from django.conf import settings
from django import forms
from django.contrib.admin import TabularInline
from django.contrib.admin.templatetags.admin_static import static


class SortableTabularInline(TabularInline):
    template = 'custom_admin/inline/sortable_tabular.html'

    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        js = ['jquery%s.js' % extra, 'jquery.init.js', 'inlines%s.js' % extra]
        if self.prepopulated_fields:
            js.extend(['urlify.js', 'prepopulate%s.js' % extra])
        if self.filter_vertical or self.filter_horizontal:
            js.extend(['SelectBox.js', 'SelectFilter2.js'])
        return forms.Media(
            js=[static('admin/js/%s' % url) for url in js] + \
               [static('js/jquery-ui-1.8.13.custom.min.js')],
            css=dict(all=[static('custom_admin/css/style.css')]))
