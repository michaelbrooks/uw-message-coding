from django.contrib.auth import get_user_model
from rest_framework import viewsets

from message_coding.apps.api import serializers
from message_coding.apps.base.permissions import IsAdminUserOrReadOnly
from message_coding.apps.base import permissions
from message_coding.apps.coding import models as coding_models
from message_coding.apps.dataset import models as dataset_models
from message_coding.apps.project import models as project_models
from message_coding.apps.dataset.filters import MessageFilterBackend


class OwnedViewSetMixin(object):
    """An api view mixin that should attach the current user on create"""
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUserOrReadOnly, )
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer


class SchemeViewSet(OwnedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = (permissions.IsProjectMember,)
    queryset = coding_models.Scheme.objects.all()
    lookup_url_kwarg = 'id'

    serializer_class = serializers.SchemeSerializer
    paginate_by = 50


class CodeGroupViewSet(viewsets.ModelViewSet):
    queryset = coding_models.CodeGroup.objects.all()
    serializer_class = serializers.CodeGroupSerializer
    paginate_by = 50


class CodeViewSet(viewsets.ModelViewSet):
    queryset = coding_models.Code.objects.all()
    serializer_class = serializers.CodeSerializer
    paginate_by = 50


class DatasetViewSet(viewsets.ModelViewSet):
    queryset = dataset_models.Dataset.objects.all()
    serializer_class = serializers.DatasetSerializer
    paginate_by = 10


class MessageViewSet(viewsets.ModelViewSet):
    queryset = dataset_models.Message.objects.all()
    serializer_class = serializers.MessageSerializer
    paginate_by = 10
    filter_backends = (MessageFilterBackend,)

    def get_queryset(self):
        task_id = self.request.query_params.get('task', None)
        if task_id is not None:
            return project_models.Task.objects.get(pk=task_id).get_messages()
        else:
            return super(MessageViewSet, self).get_queryset()

class ProjectViewSet(OwnedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = (permissions.IsProjectMember, permissions.IsProjectOwnerOrReadOnly,)
    queryset = project_models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    paginate_by = 10


class TaskViewSet(OwnedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = (permissions.IsTaskAssigner, permissions.IsTaskOwnerOrReadOnly,)
    queryset = project_models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
    paginate_by = 10


class CodeInstanceViewSet(OwnedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = (permissions.IsTaskAssigner, permissions.IsTaskOwnerOrReadOnly,)
    queryset = project_models.CodeInstance.objects.all()
    serializer_class = serializers.CodeInstanceSerializer
    paginate_by = 100

    def get_queryset(self):
        queryset = super(CodeInstanceViewSet, self).get_queryset()

        owner = self.request.query_params.get('owner', None)
        if owner is not None:
            queryset = queryset.filter(owner=owner)

        task = self.request.query_params.get('task', None)
        if task is not None:
            queryset = queryset.filter(task=task)

        return queryset
