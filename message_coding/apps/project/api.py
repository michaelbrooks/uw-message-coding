from rest_framework import serializers, viewsets, routers
from base.views import OwnedViewSetMixin

from apps.project.models import Project, Task
from apps.dataset import models as dataset_models
from apps.dataset.api import SelectionSerializer

# Serializers define the API representation.
class TaskSerializer(serializers.ModelSerializer):
    selection = SelectionSerializer()

    class Meta:
        model = Task
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
        model = Project
        fields = ('id', 'name', 'description',
                  'slug', 'created_at', 'owner', 'members',
                  'tasks', 'schemes', 'datasets')


# ViewSets define the view behavior.
class ProjectViewSet(OwnedViewSetMixin, viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    paginate_by = 10


class TaskViewSet(OwnedViewSetMixin, viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    paginate_by = 10


# Routers provide an easy way of automatically determining the URL conf.
router = routers.SimpleRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'tasks', TaskViewSet)
