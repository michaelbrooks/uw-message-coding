from rest_framework import viewsets
from base.views import OwnedViewSetMixin
from apps.dataset.api import serializers
from apps.dataset import models
from apps.dataset.filters import MessageFilterBackend


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

    # def get_queryset(self):
    #
    # selection_id = self.request.query_params.get('selection_id', None)
    #     if selection_id is not None:
    #         selection = models.Selection.objects.get(pk=selection_id)
    #         return selection.get_messages()
    #
    #     queryset = models.Message.objects.all()
    #
    #     dataset_id = self.request.query_params.get('dataset_id', None)
    #     if dataset_id is not None:
    #         return queryset.filter(dataset_id=dataset_id)
    #
    #     return queryset
