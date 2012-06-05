# -*- coding: utf-8 -*-

from django import forms
from django.template import Context
from django.template.loader import get_template
from django.utils.safestring import mark_safe

from markitup.widgets import AdminMarkItUpWidget


class TeaserPreviewWidget(AdminMarkItUpWidget):

    class Media:
        css = dict(all=(
            '/static/css/widgets/teaser_preview.css',
            '/static/css/fonts/MyFonts Webfonts Order M2655697.css',
            'http://fonts.googleapis.com/css?family=PT+Serif:400,700,400italic,700italic&subset=latin,cyrillic',
            ), )
        js = ('/static/js/teaser_preview.js', )

    def render(self, name, value, attrs=None):
        value = super(TeaserPreviewWidget, self).render(name, value, attrs)
        ctx = dict(lang=attrs['id'][-2:])
        tpl = get_template('storage/teaser_preview.html')
        preview = tpl.render(Context(ctx))
        return mark_safe('%s %s' % (preview, value))
