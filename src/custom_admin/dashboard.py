# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name

from . dashdesc import chunks_common
from .. storage.dashdesc import storage_common


class CustomIndexDashboard(Dashboard):
    u"""Настройка отображения админки."""

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        self.children.append(
            modules.LinkList(_(u'Quick links'),
                layout='inline',
                draggable=False,
                deletable=False,
                collapsible=False,
                children=[
                    [_(u'Return to site'), reverse('frontend:index')],
                    [_(u'Error Console'), reverse('sentry')],
                    [_(u'Change password'), reverse('%s:password_change' % site_name)],
                    [_(u'Log out'), reverse('%s:logout' % site_name)], ]))

        self.children.append(modules.RecentActions(_(u'Recent Actions'), 5))

        self.children.append(modules.Feed(
                    _(u'Latest Django News'),
                    feed_url='http://www.djangoproject.com/rss/weblog/',
                    limit=10))

        self.children.append(
            modules.LinkList(
                _(u'Support'),
                children=[
                    dict(
                        title=_(u'Django documentation (RU)'),
                        url='http://djbook.ru/rel1.4/',
                        external=True),
                    dict(
                        title=_(u'Django documentation (EN)'),
                        url='http://docs.djangoproject.com/',
                        external=True),
                    dict(
                        title=_(u'Django "django-users" mailing list'),
                        url='http://groups.google.com/group/django-users',
                        external=True),
                    dict(
                        title=_(u'Django irc channel'),
                        url='irc://irc.freenode.net/django',
                        external=True),
                ]))

        self.children.append(storage_common())
        self.children.append(chunks_common())
        # self.children.append(ImageDropZone())


class CustomAppIndexDashboard(AppIndexDashboard):
    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        super(CustomAppIndexDashboard, self).__init__(*args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
