# -*- coding: utf-8 -*-

from haystack import indexes
from haystack import site

from . models import Project


class ProjectIndex(indexes.SearchIndex):
    description = indexes.CharField(document=True, use_template=True)
    customer = indexes.CharField(model_attr='customer')
    registered = indexes.DateTimeField(model_attr='registered')

    def index_queryset(self):
        return Project.objects.all()

site.register(Project, ProjectIndex)
