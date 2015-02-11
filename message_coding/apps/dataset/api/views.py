from rest_framework import viewsets
from base.views import OwnedViewSetMixin
from apps.dataset.api import serializers
from apps.dataset import models
from apps.dataset.filters import MessageFilterBackend
from apps.project import models as project_models

# ViewSets define the view behavior.
class DatasetViewSet(viewsets.ModelViewSet):
    queryset = models.Dataset.objects.all()
    serializer_class = serializers.DatasetSerializer
    paginate_by = 10


class SelectionViewSet(OwnedViewSetMixin, viewsets.ModelViewSet):
    queryset = models.Selection.objects.all()
    serializer_class = serializers.SelectionSerializer
    paginate_by = 10


class MessageViewSet(viewsets.ModelViewSet):
    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializer
    paginate_by = 10
    filter_backends = (MessageFilterBackend,)
    
    def get_queryset(self):
        task_id = self.request.query_params.get('task', None)
        if task_id is not None:
            return project_models.Task.objects.get(pk=task_id).selection.get_messages()
        else:
            return super(MessageViewSet, self).get_queryset()
