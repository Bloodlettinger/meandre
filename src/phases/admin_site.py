# -*- coding: utf-8 -*-

from django.contrib.admin.sites import AdminSite
from django.views.decorators.cache import never_cache
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages

from . import models
from . import forms

PHASES_MAX_STEP = 6


class PhasesWizardAdmin(AdminSite):

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url
        urls = patterns(
            '',
            url(r'^input/(?P<pk>\d+)/(?P<step>\d+)/$', self.admin_view(self.input), name='input'),
            url(r'^project/(?P<pk>\d+)/$', self.admin_view(self.project), name='project'),
            )
        urls += super(PhasesWizardAdmin, self).get_urls()
        return urls

    def has_permission(self, request):
        return request.user.is_active

    @never_cache
    def input(self, request, pk, step, extra_context=None):
        step = int(step)
        if request.method == 'POST' and 'back' in request.POST and step > 1:
            return redirect('phases:input', pk=pk, step=step - 1)

        from .. storage.models import Project
        project = get_object_or_404(Project, pk=pk)
        created = models.Relation.assign_phases_on(project)
        if created:
            messages.info(request, _(u'Phase set is created for project <%s>.' % unicode(project)))

        phase = get_object_or_404(models.Phase, pk=step)
        qs = models.Relation.objects.select_related(depth=1).filter(project__pk=pk, step__phase=step)

        if request.method == 'POST':
            formset = forms.PhasesFormSet(request.POST)
            if formset.is_valid():
                # сохраняем данные страницы в сессии
                data = {'phase_%i' % step: formset.cleaned_data, }
                phases = request.session.get('phases', dict())
                phases.update(data)
                request.session['phases'] = phases

                if step < PHASES_MAX_STEP:
                    return redirect('phases:input', pk=pk, step=step + 1)
                else:
                    phases = request.session.get('phases', {})
                    if PHASES_MAX_STEP == len(phases.keys()):
                        # сохраняем расценки этапов проекта
                        for phase in phases.values():
                            for step in phase:
                                relation = step.pop('id')
                                for field, value in step.items():
                                    setattr(relation, field, value)
                                relation.save()
                        return redirect('phases:project', pk=pk)
                    else:
                        messages.error(request,
                            _(u'It seems you have missed some steps, go back.'))
                        return redirect('phases:input', pk=pk, step=1)
            else:
                # при ошибках в наборе форм возвращаемся обратно
                messages.error(request,
                    _(u'Errors: %s') % formset.errors)
                return redirect('phases:input', pk=pk, step=step)
        else:
            formset = forms.PhasesFormSet(None, queryset=qs)

        context = dict(
            formset=formset,
            phase=phase,
            step=step,
            )
        return TemplateResponse(request, 'phases/wizard_input.html', context)

    @never_cache
    def project(self, request, pk, extra_context=None):
        from .. storage.models import Project
        project = get_object_or_404(Project, pk=pk)
        qs = models.Phase.objects.filter(step__relation__project=project).distinct()
        context = dict(phases=qs)
        return TemplateResponse(request, 'phases/cost_card.html', context)


site = PhasesWizardAdmin(name=u'phases')
