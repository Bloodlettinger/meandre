# -*- coding: utf-8 -*-

from datetime import date

from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template

from haystack.query import SearchQuerySet

from src.storage import models

from . forms import MainSearchForm


def index(request):
    year = date.today().year

    context = dict(
        projects=models.Project.objects.winned().public(),
        clients=models.Customer.objects.filter(logo__isnull=False, url__isnull=False),
        recommendations=models.Recommendation.objects.all(),
        all_job_types=models.JobType.objects.all(),
        stat=models.Project.statistic.compare_years(year, year - 1)
    )
    return direct_to_template(request, 'frontend/index.html', context)


def search(request):
    form = MainSearchForm(request.GET or None)

    context = dict(form=form)

    if form.is_valid():
        query = form.cleaned_data.get('query', '')
        sqs = SearchQuerySet().filter(description=query)
        context = dict(context,
            projects=models.Project.objects.filter(pk__in=[i.pk for i in sqs]),
            searching_for=query)
    return direct_to_template(request, 'frontend/search.html', context)


def project(request, slug):
    obj = get_object_or_404(models.Project, slug=slug)

    role_users = dict()
    for membership in obj.membership_set.all():
        for role in membership.role.all():
            staff = role_users.get(role.name, list())
            if membership.user:
                staff.append(membership.user)
            elif membership.company:
                staff.append(membership.company)
            role_users[role.name] = staff

    context = dict(
        project=obj,
        next=models.Project.objects.get_next(obj),
        prev=models.Project.objects.get_prev(obj),
        all_job_types=models.JobType.objects.all(),
        roles=role_users,
    )
    return direct_to_template(request, 'frontend/project.html', context)
