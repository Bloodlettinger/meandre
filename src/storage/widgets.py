# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from django.utils.safestring import mark_safe

from markitup.widgets import AdminMarkItUpWidget


class TeaserPreviewWidget(AdminMarkItUpWidget):

    class Media:
        css = dict(all=(
            settings.STATIC_URL + 'css/widgets/teaser_preview.css',
            settings.STATIC_URL + 'css/fonts/MyFonts Webfonts Order M2655697.css',
            'http://fonts.googleapis.com/css?family=PT+Serif:400,700,400italic,700italic&subset=latin,cyrillic',
            ), )
        js = (settings.STATIC_URL + 'js/teaser_preview.js', )

    def render(self, name, value, attrs=None):
        value = super(TeaserPreviewWidget, self).render(name, value, attrs)
        ctx = dict(lang=attrs['id'][-2:])
        tpl = get_template('storage/teaser_preview.html')
        preview = tpl.render(Context(ctx))
        return mark_safe('%s %s' % (preview, value))


class HorizontalRadioRenderer(forms.RadioSelect.renderer):

    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class RadioSelectHorizontal(forms.RadioSelect):

    renderer = HorizontalRadioRenderer

    class Media:
        css = dict(all=(
            settings.STATIC_URL + 'css/custom_admin.css',
            ), )
