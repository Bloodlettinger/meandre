# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from admin_tools.dashboard.modules import DashboardModule


class ImageDropZone(DashboardModule):

    title = _(u'Image Drop Zone')
    template = 'uploader/admin_tools.html'

    def __init__(self, *args, **kwargs):
        super(ImageDropZone, self).__init__(*args, **kwargs)

    def init_with_context(self, context):
        if self._initialized:
            return

        self.children.append('stub for parent class logic')
        self._initialized = True
