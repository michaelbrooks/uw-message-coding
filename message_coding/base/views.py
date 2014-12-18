""" Views for the base application """

from django.shortcuts import render

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.utils.translation import ugettext as _
from django.apps import apps

def home(request):
    """ Default view for the root """
    return render(request, 'base/home.html')


class ProjectUrlMixin(object):
    """A mixin that looks in the url
      for a project_pk value, adds the associated
      project to the template context, and adds a
      self.project attribute to the view."""

    def get_project(self):
        if not hasattr(self, 'project'):
            Project = apps.get_model('project.Project')

            project_pk = self.kwargs['project_pk']

            try:
                project = Project.objects.get(pk=project_pk)
            except ObjectDoesNotExist:
                raise Http404(_("No %(verbose_name)s found") %
                              {'verbose_name': Project._meta.verbose_name})

            self.project = project
        return self.project

    def get_context_data(self, **kwargs):
        kwargs['project'] = self.get_project()
        return super(ProjectUrlMixin, self).get_context_data(**kwargs)
