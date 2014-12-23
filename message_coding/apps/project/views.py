
from django.views.generic import CreateView, DetailView

import models
from django.apps import apps
from apps.dataset import models as dataset_models
from django.http import HttpResponse
from django.template import Context,loader
from base.views import ProjectUrlMixin, LoginRequiredMixin
from django.core.urlresolvers import reverse 

def index(request):
    Project = apps.get_model('project.Project')
    project = Project.objects.get(owner_id = request.user)
    t = loader.get_template('project/dash_detail.html')
    c = Context({'project':project,})
    return HttpResponse(t.render(c))


class CreateProjectView(LoginRequiredMixin,CreateView):
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
    
class ProjectDetailView(LoginRequiredMixin,DetailView):
    """View for viewing projects"""
    model = models.Project
    template_name = 'project/project_detail.html'
    prefetch_related = ['datasets']


class TaskDetailView(LoginRequiredMixin, ProjectUrlMixin, DetailView):
    """View for viewing tasks"""
    model = models.Task
    template_name = 'project/task_detail.html'


class CreateTaskView(LoginRequiredMixin, ProjectUrlMixin, CreateView):
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


class DatasetImport(LoginRequiredMixin, ProjectUrlMixin, CreateView):
    """ View for importing a dataset """

    model = dataset_models.Dataset
    fields = ['name', 'description' ]
    template_name = "project/dataset_import.html"

    def get_success_url(self):
        return reverse('dataset_details', kwargs={ 'project_pk': self.get_project().id, 'dataset_pk': self.object.id})


    def form_valid(self, form):
        # The user comes from the session
        form.instance.owner = self.request.user

        # This comes from the URL
        project = self.get_project()
        form.instance.save()
        form.instance.projects.add(project)


        return super(DatasetImport, self).form_valid(form)




class DatasetDetails(LoginRequiredMixin, ProjectUrlMixin, DetailView):
    """ View for dataset details """

    model = dataset_models.Dataset
    fields = ['name', 'description']
    template_name = "project/dataset_detail.html"

    slug_field = 'id'
    slug_url_kwarg = 'dataset_pk'




