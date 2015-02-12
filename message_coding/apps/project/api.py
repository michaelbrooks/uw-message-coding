from rest_framework import serializers, viewsets, routers
from base.views import OwnedViewSetMixin
from base.permissions import IsProjectMember, IsProjectOwnerOrReadOnly, IsTaskAssigner, IsTaskOwnerOrReadOnly

from apps.project import models as project_models
from apps.dataset import models as dataset_models
from apps.dataset.api import serializers as dataset_serializers

# Serializers define the API representation.
class TaskSerializer(serializers.ModelSerializer):
    selection = dataset_serializers.SelectionSerializer()

    class Meta:
        model = project_models.Task
        fields = ('id', 'name', 'description', 'selection',
                  'created_at', 'owner', 'project', 'scheme', 'assigned_coders')
        read_only_fields = ('created_at', 'owner',)


    def create(self, validated_data):
        # Create the nested selection
        selection_data = validated_data.pop('selection')
        if 'owner' not in selection_data:
            selection_data['owner'] = validated_data['owner']

        selection = dataset_models.Selection.objects.create(**selection_data)
        validated_data['selection'] = selection
        return super(TaskSerializer, self).create(validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = project_models.Project
        fields = ('id', 'name', 'description',
                  'slug', 'created_at', 'owner', 'members',
                  'tasks', 'schemes', 'datasets')
        read_only_fields = ('created_at', 'owner',)


class CodeInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = project_models.CodeInstance
        fields = ('id', 'created_at',
                  'owner', 'task',
                  'message', 'code',)
        read_only_fields = ('created_at', 'owner',)

# ViewSets define the view behavior.
class ProjectViewSet(OwnedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = (IsProjectMember, IsProjectOwnerOrReadOnly,)
    queryset = project_models.Project.objects.all()
    serializer_class = ProjectSerializer
    paginate_by = 10


class TaskViewSet(OwnedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = (IsTaskAssigner, IsTaskOwnerOrReadOnly,)
    queryset = project_models.Task.objects.all()
    serializer_class = TaskSerializer
    paginate_by = 10


class CodeInstanceViewSet(OwnedViewSetMixin, viewsets.ModelViewSet):
    queryset = project_models.CodeInstance.objects.all()
    serializer_class = CodeInstanceSerializer
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

# Routers provide an easy way of automatically determining the URL conf.
router = routers.SimpleRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'code_instances', CodeInstanceViewSet)
