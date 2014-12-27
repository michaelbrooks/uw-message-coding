from django.views.generic import CreateView, DetailView
from django.apps import apps
from django.http import HttpResponse
from django.template import Context, loader
from apps.project import forms, models
from apps.dataset import models as dataset_models
from base.views import ProjectViewMixin, LoginRequiredMixin


def index(request):
    Project = apps.get_model('project.Project')
    project = Project.objects.get(owner_id=request.user)
    t = loader.get_template('project/dash_detail.html')
    c = Context({'project': project, })
    return HttpResponse(t.render(c))


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








