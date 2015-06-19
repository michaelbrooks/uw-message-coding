from django.views.generic import CreateView, DetailView, UpdateView
from django import http
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

from rest_framework.renderers import JSONRenderer

from message_coding.apps.api import serializers
from message_coding.apps.project import models, forms
from message_coding.apps.coding import models as coding_models
from message_coding.apps.base.views import ProjectViewMixin, LoginRequiredMixin


class CreateProjectView(LoginRequiredMixin, CreateView):
    """View for creating new projects"""

    form_class = forms.ProjectForm

    template_name = "project/project_create.html"

    def form_valid(self, form):
        """What to do when a project is created?"""

        # The user comes from the session
        form.instance.owner = self.request.user

        return super(CreateProjectView, self).form_valid(form)


class UpdateProjectView(LoginRequiredMixin, UpdateView):
    """View for editing projects"""

    model = models.Project
    form_class = forms.ProjectForm
    slug_url_kwarg = 'project_slug'

    template_name = "project/project_update.html"



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

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        context['msgs'] = context['task'].selection.get_messages()
        task = context['task']
        return context

class TaskReviewView(LoginRequiredMixin, ProjectViewMixin, DetailView):
    """View for viewing tasks"""
    model = models.Task
    template_name = 'project/task_review.html'

    pk_url_kwarg = 'task_pk'

    def get_context_data(self, **kwargs):
        context = super(TaskReviewView, self).get_context_data(**kwargs)
        context['msgs'] = context['task'].selection.get_messages()
        task = context['task']
        examples = task.get_examples()
        frequency = task.get_frequency()
        context['summary'] = task.get_coding_summary()
        context['diff_summary'] = task.get_diff_summary()
        code_info = {}
        for code,count in frequency.iteritems():
            code_info[code] = {
                'count':count,
                'examples':examples[code]
            }
        context['code_info'] =  code_info
        return context

class EditTaskView(LoginRequiredMixin, ProjectViewMixin, UpdateView):
    """View for editing new tasks"""

    model = models.Task
    pk_url_kwarg = 'task_pk'

    # Let Django autogenerate the form for now
    fields = ['name', 'description', 'scheme', 'assigned_coders']

    template_name = "project/task_edit.html"


CODING_BATCH_SIZE = 1


class CodingView(LoginRequiredMixin, ProjectViewMixin, DetailView):
    """
    View for working on a coding task.
    This is implemented as a detailview for coding tasks.
    """

    model = models.Task
    template_name = "project/coding.html"
    pk_url_kwarg = 'task_pk'

    def get_object(self, queryset=None):
        obj = super(CodingView, self).get_object(queryset)

        # Ensure the user is assigned to code this
        if not obj.is_assigned_to(self.request.user):
            raise PermissionDenied("You are not assigned to that task.")

        return obj

    def get_messages(self):
        task = self.object
        user = self.request.user

        # Ensure the user is assigned to code this
        if not task.is_assigned_to(user):
            raise PermissionDenied("You are not assigned to that task.")

        try:
            self.page = int(self.kwargs.get('page', 1))
        except ValueError:
            self.page = 1

        # Get the messages to code
        self.paginator = Paginator(task.selection.get_messages(), CODING_BATCH_SIZE)

        try:
            self.page = self.paginator.validate_number(self.page)

        except PageNotAnInteger:
            # If page is not an integer, go to the first page.
            self.page = 1

        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            self.page = self.paginator.num_pages

        return self.paginator.page(self.page)


    def get_context_data(self, **kwargs):
        # Add some serialized json for bootstrapping the client-side app
        renderer = JSONRenderer()

        task = self.object
        kwargs['project_json'] = renderer.render(serializers.ProjectSerializer(self.get_project()).data)
        kwargs['task_json'] = renderer.render(serializers.TaskSerializer(self.object).data)
        kwargs['user_json'] = renderer.render(serializers.UserSerializer(self.request.user).data)
        kwargs['code_scheme_json'] = renderer.render(serializers.SchemeSerializer(task.scheme).data)

        return super(CodingView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        task = self.object

        # The messages we expect to be coding
        msgs = self.get_messages()

        # Get all the legal code ids for this task's scheme
        all_code_ids = coding_models.Code.objects \
            .filter(code_group__in=task.scheme.code_groups.all()) \
            .values_list('pk', flat=True)
        all_code_ids = set(all_code_ids)  # for fast lookup

        # Extract all the new code ids for each message from the POST params
        message_code_ids = {}
        for msg in msgs:
            key = "messages[%d]" % msg.pk
            message_code_ids[msg.pk] = set()
            for code_id in self.request.POST.getlist(key):
                code_id = int(code_id)  # convert str to int

                if code_id not in all_code_ids:
                    return http.HttpResponseBadRequest("Code id %d not allowed" % code_id)

                message_code_ids[msg.pk].add(code_id)

        # Make sure all the messages match up
        if not message_code_ids or len(message_code_ids) != len(msgs):
            return http.HttpResponseBadRequest("Invalid set of messages coded")

        # Now create/delete instances as needed
        to_create = []
        to_delete = []
        for msg in msgs:
            current_instances = models.CodeInstance.objects \
                .filter(owner=self.request.user,
                        task=task,
                        message=msg) \
                .only('pk', 'code_id')

            new_code_ids = message_code_ids[msg.pk]

            for inst in current_instances:
                if inst.code_id not in new_code_ids:
                    # it has been un-checked
                    to_delete.append(inst)
                else:
                    # it is in both
                    new_code_ids.remove(inst.code_id)

            for code_id in new_code_ids:
                # any left over must be created
                to_create.append(models.CodeInstance(owner=self.request.user,
                                                     task=task,
                                                     message=msg,
                                                     code_id=code_id))

        models.CodeInstance.objects \
            .filter(pk__in=[inst.pk for inst in to_delete]) \
            .delete()

        models.CodeInstance.objects.bulk_create(to_create)

        next_page = self.page + 1
        return redirect('coding_page', project_slug=task.project.slug, task_pk=task.pk, page=next_page)
