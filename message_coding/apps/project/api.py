from rest_framework import serializers, viewsets, routers

from apps.project.models import Project, Task


# Serializers define the API representation.
class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', 'description',
                  'created_at', 'owner', 'project', 'scheme', 'assigned_coders')


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description',
                  'slug', 'created_at', 'owner', 'members',
                  'tasks', 'schemes', 'datasets')


# ViewSets define the view behavior.
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    paginate_by = 10


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    paginate_by = 10


# Routers provide an easy way of automatically determining the URL conf.
router = routers.SimpleRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'tasks', TaskViewSet)
