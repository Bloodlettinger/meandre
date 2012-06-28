# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from admin_tools.dashboard import modules


def chunks_common():
    return modules.ModelList(_(u'Static Blocks'), [
        'chunks.models.Chunk',
        'chunks.models.Image',
        'chunks.models.Media',
        ])
