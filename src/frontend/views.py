# -*- coding: utf-8 -*-

from random import shuffle
from datetime import date

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from django.utils import translation

from haystack.query import SearchQuerySet

from ..storage import models
from ..uploader.models import Queue as ProjectImages

from . forms import MainSearchForm


def index(request):
    year = date.today().year
    customers = list(models.Customer.objects.select_related(depth=1).filter(
        project__status=2,  # выигранные
        url__isnull=False
        ).exclude(logo=u'').distinct())
    shuffle(customers)
    teasers = models.Teaser.objects.filter(
        visible=True,
        lang=translation.get_language()[:2])
    context = dict(
        teasers=teasers,
        projects=models.Project.objects.select_related(depth=1).winned().public().order_by('-begin'),
        clients=customers,
        recommendations=models.Recommendation.objects.all(),
        all_job_types=models.JobType.objects.all(),
        dirs=models.Project.statistic.directions(),
        stat=models.Project.statistic.compare_years(year, year - 1),
        ctype=models.Customer.statistic.types()
    )
    return direct_to_template(request, 'frontend/index.html', context)


def search(request):
    form = MainSearchForm(request.GET or None)

    context = dict(form=form)

    if form.is_valid():
        query = form.cleaned_data.get('query', '')
        sqs = SearchQuerySet().filter(description=query)

        params = {
            u'pk__in': [i.pk for i in sqs],
            u'is_public_%s' % translation.get_language()[:2]: True
        }
        projects = models.Project.objects.select_related(depth=1).filter(**params)

        if not request.user.is_authenticated():
            projects = projects.winned().public()
        context = dict(context,
            projects=projects,
            searching_for=query)
    return direct_to_template(request, 'frontend/search.html', context)


def project(request, slug):
    obj = get_object_or_404(models.Project, **{
        'slug': slug,
        u'is_public_%s' % translation.get_language()[:2]: True
    })

    context = dict(
        project=obj,
        images=ProjectImages.objects.select_related().filter(tags=obj.code, visible=True).order_by('position'),
        next=models.Project.objects.select_related(depth=1).get_next(obj),
        prev=models.Project.objects.select_related(depth=1).get_prev(obj),
        all_job_types=models.JobType.objects.all(),
        membership_set=models.Membership.objects.select_related(depth=1).filter(project=obj)
    )
    return direct_to_template(request, 'frontend/project.html', context)


def lang(request, code):
    next = request.META.get('HTTP_REFERER', '/')
    response = HttpResponseRedirect(next)
    if code and translation.check_for_language(code):
        if hasattr(request, 'session'):
            request.session['django_language'] = code
        else:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, code)
        translation.activate(code)
    return response
