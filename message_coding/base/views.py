""" Views for the base application """

from django.shortcuts import render

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.utils.translation import ugettext as _
from django.apps import apps
from django.contrib.auth.decorators import login_required

def home(request):
    """ Default view for the root """
    return render(request, 'base/home.html')


class ProjectViewMixin(object):
    """A mixin that looks in the url
      for a project_pk or project_slug value, adds the associated
      project to the template context, and adds a
      self.project attribute to the view."""

    def get_project(self):
        if not hasattr(self, 'project'):
            Project = apps.get_model('project.Project')

            try:
                if 'project_pk' in self.kwargs:
                    self.project = Project.objects.get(pk=self.kwargs['project_pk'])
                elif 'project_slug' in self.kwargs:
                    self.project = Project.objects.get(slug=self.kwargs['project_slug'])
            except ObjectDoesNotExist:
                raise Http404(_("No %(verbose_name)s found") %
                              {'verbose_name': Project._meta.verbose_name})

        return self.project

    def get_context_data(self, **kwargs):
        kwargs['project'] = self.get_project()
        return super(ProjectViewMixin, self).get_context_data(**kwargs)



class LoginRequiredMixin(object):
    """A mixin that forces a login to view the CBTemplate."""
    
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)
