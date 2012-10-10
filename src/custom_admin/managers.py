# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone

from .. storage import models as storage


class SalesReportManager(models.Manager):

    def get_query_set(self):
        return super(SalesReportManager, self).get_query_set().filter(
            status=storage.PROJECT_STATUS_WON,
            begin__year=timezone.now().year
        ).order_by('-begin')
