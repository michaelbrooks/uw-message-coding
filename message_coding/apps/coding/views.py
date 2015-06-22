from django.views.generic import DetailView
from rest_framework.renderers import JSONRenderer

from message_coding.apps.coding import models
from message_coding.apps.base.views import LoginRequiredMixin, ProjectViewMixin
from message_coding.apps.api import serializers


class SchemeEditorView(LoginRequiredMixin, ProjectViewMixin, DetailView):
    """View for viewing datasets"""
    model = models.Scheme
    template_name = 'coding/scheme_editor.html'
    pk_url_kwarg = 'scheme_pk'

    def get_context_data(self, **kwargs):
        # Add some serialized json for bootstrapping the client-side app
        renderer = JSONRenderer()
        kwargs['project_json'] = renderer.render(serializers.ProjectSerializer(self.get_project()).data)
        kwargs['scheme_json'] = renderer.render(serializers.SchemeSerializer(self.object).data)
        kwargs['user_json'] = renderer.render(serializers.UserSerializer(self.request.user).data)

        return super(SchemeEditorView, self).get_context_data(**kwargs)
