from django.views.generic import CreateView, DetailView
from django.core.urlresolvers import reverse

from message_coding.apps.coding import models
from message_coding.apps.base.views import LoginRequiredMixin, ProjectViewMixin

from message_coding.apps.coding.api import SchemeSerializer
from message_coding.apps.base.api import UserSerializer
from message_coding.apps.project import api as project_api
from rest_framework.renderers import JSONRenderer


class SchemeEditorView(LoginRequiredMixin, ProjectViewMixin, DetailView):
    """View for viewing datasets"""
    model = models.Scheme
    template_name = 'coding/scheme_editor.html'
    pk_url_kwarg = 'scheme_pk'

    def get_context_data(self, **kwargs):
        # Add some serialized json for bootstrapping the client-side app
        renderer = JSONRenderer()
        kwargs['project_json'] = renderer.render(project_api.ProjectSerializer(self.get_project()).data)
        kwargs['scheme_json'] = renderer.render(SchemeSerializer(self.object).data)
        kwargs['user_json'] = renderer.render(UserSerializer(self.request.user).data)

        return super(SchemeEditorView, self).get_context_data(**kwargs)
