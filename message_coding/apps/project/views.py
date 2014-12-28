from django.views.generic import CreateView, DetailView

from apps.project import models, forms
from apps.dataset import models as dataset_models
from base.views import ProjectViewMixin, LoginRequiredMixin, TaskViewMixin
from django.core.urlresolvers import reverse 


class CreateProjectView(LoginRequiredMixin, CreateView):
    """View for creating new projects"""

    form_class = forms.ProjectCreateForm

    template_name = "project/project_create.html"

    def form_valid(self, form):
        """What to do when a project is created?"""

        # The user comes from the session
        form.instance.owner = self.request.user

        return super(CreateProjectView, self).form_valid(form)



class ProjectDetailView(LoginRequiredMixin, DetailView):
    """View for viewing projects"""
    model = models.Project
    template_name = 'project/project_detail.html'
    prefetch_related = ['datasets']

    slug_url_kwarg = 'project_slug'


class TaskDetailView(LoginRequiredMixin, ProjectViewMixin, DetailView):
    """View for viewing tasks"""
    model = models.Task
    template_name = 'project/task_detail.html'

    pk_url_kwarg = 'task_pk'


class CreateTaskView(LoginRequiredMixin, ProjectViewMixin, CreateView):
    """View for creating new tasks"""

    model = models.Task

    # Let Django autogenerate the form for now
    fields = ['name', 'description', 'scheme', 'assigned_coders']

    template_name = "project/task_create.html"

    def form_valid(self, form):
        """What to do when a task is created?"""

        # The user comes from the session
        form.instance.owner = self.request.user

        # This comes from the URL
        project = self.get_project()
        form.instance.project = project

        # This selection thing is hard-coded for now
        dataset = project.datasets.first()
        selection = dataset_models.Selection(
            owner=self.request.user,
            dataset=dataset
        )
        selection.save()

        form.instance.selection = selection

        return super(CreateTaskView, self).form_valid(form)


CODING_BATCH_SIZE = 1
class CodingView(LoginRequiredMixin, ProjectViewMixin, DetailView):
    """
    View for working on a coding task.
    This is implemented as a detailview for coding tasks.
    """

    model = models.Task
    template_name = "project/coding.html"


class TaskMessagesView(LoginRequiredMixin, ProjectViewMixin, TaskViewMixin, DetailView):
    """Gets messages for a coding task."""

