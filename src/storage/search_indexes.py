# -*- coding: utf-8 -*-

from __future__ import absolute_import

from haystack import site
from haystack import indexes

from . import models


class ProjectIndex(indexes.RealTimeSearchIndex):
    description = indexes.CharField(document=True, use_template=True)
    customer = indexes.CharField(model_attr='customer')
    registered = indexes.DateTimeField(model_attr='registered')

    def index_queryset(self):
        return models.Project.objects.all()

site.register(models.Project, ProjectIndex)
