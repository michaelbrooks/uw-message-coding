
from django.views.generic import CreateView, DetailView


import models
from apps.dataset import models as dataset_models
from base.views import ProjectUrlMixin
class CreateProjectView(CreateView):
    """View for creating new projects"""

    model = models.Project

    # Let Django autogenerate the form for now
    fields = ['name', 'description', 'members']

    template_name = "project/project_create.html"

    def form_valid(self, form):
        """What to do when a project is created?"""

        # The user comes from the session
        # TODO: require logging in
        form.instance.owner = self.request.user


        return super(CreateProjectView, self).form_valid(form)

class ProjectDetailView(DetailView):
    """View for viewing projects"""
    model = models.Project
    template_name = 'project/project_detail.html'

class TaskDetailView(ProjectUrlMixin, DetailView):
    """View for viewing tasks"""
    model = models.Task
    template_name = 'project/task_detail.html'


class CreateTaskView(ProjectUrlMixin, CreateView):
    """View for creating new tasks"""

    model = models.Task

    # Let Django autogenerate the form for now
    fields = ['name', 'description', 'scheme', 'assigned_coders']

    template_name = "project/task_create.html"

    def form_valid(self, form):
        """What to do when a task is created?"""

        # The user comes from the session
        # TODO: require logging in
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

