# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from admin_tools.menu import items, Menu


class CustomMenu(Menu):
    """
    Custom Menu for sag admin site.
    """
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children += [
            items.MenuItem(_('Dashboard'), reverse('admin:index')),
            items.Bookmarks(),
            items.AppList(
                _('Applications'),
                exclude=('django.contrib.*',)
            ),
            items.AppList(
                _('Administration'),
                models=('django.contrib.*',)
            ),
            items.ModelList(_(u'Workflow'), [
                'src.storage.models.Customer',
                'src.storage.models.Project',
                ]),
            items.ModelList(_(u'Finances'), [
                'src.storage.models.FinanceTransaction',
                ]),
            items.ModelList(_(u'Dictionaries'), [
                'src.storage.models.Workarea',
                'src.storage.models.JobType',
                ]),
            items.ModelList(_(u'Static Blocks'), [
                'chunks.models.Chunk',
                'chunks.models.Image',
                'chunks.models.Media',
                ]),
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomMenu, self).init_with_context(context)
