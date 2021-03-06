""" Views for the base application """

from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth import get_user_model

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
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

                # Make sure the user is part of this project
                if not self.project.has_member(self.request.user):
                    raise PermissionDenied("You are not a member of that project.")

            except ObjectDoesNotExist:
                raise Http404(_("No %(verbose_name)s found") %
                              {'verbose_name': Project._meta.verbose_name})

        return self.project

    def get_context_data(self, **kwargs):
        kwargs['project'] = self.get_project()
        return super(ProjectViewMixin, self).get_context_data(**kwargs)


class TaskViewMixin(ProjectViewMixin):
    """A mixin that looks in the url
      for a task_pk, adds the associated
      task to the template context, and adds a
      self.task attribute to the view.
      Also includes functionality of ProjectViewMixin."""

    def get_task(self):
        if not hasattr(self, 'task'):
            Task = apps.get_model('project.Task')

            try:
                if 'task_pk' in self.kwargs:
                    self.task = Task.objects.get(pk=self.kwargs['task_pk'])

                    if self.task.project != self.get_project():
                        raise Http404(_("That task is not in that project"))

            except ObjectDoesNotExist:
                raise Http404(_("No %(verbose_name)s found") %
                              {'verbose_name': Task._meta.verbose_name})

        return self.task

    def get_context_data(self, **kwargs):
        kwargs['task'] = self.get_task()
        return super(TaskViewMixin, self).get_context_data(**kwargs)


class LoginRequiredMixin(object):
    """A mixin that forces a login to view the CBTemplate."""
    
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class UserDashboard(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'base/dash_detail.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(UserDashboard, self).get_context_data(**kwargs)

        # todo: filter to just open tasks
        user = self.object
        open_tasks = []
        for project in user.projects.all():
            open_tasks.extend(project.tasks.all())
        context['open_tasks'] = open_tasks

        return context

