from apps.dataset.models import Dataset, Selection, Message
from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.
class DatasetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dataset
        fields = ('id', 'name', 'description', 'slug', 'created_at',
                  'owner', 'projects')


class SelectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Selection
        fields = ('id', 'created_at', 'owner', 'dataset', 'type', 'selection', 'size')


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'sender', 'time', 'text', 'dataset')


# ViewSets define the view behavior.
class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    paginate_by = 10


class SelectionViewSet(viewsets.ModelViewSet):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    paginate_by = 10


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    paginate_by = 100

# Routers provide an easy way of automatically determining the URL conf.
router = routers.SimpleRouter()
router.register(r'datasets', DatasetViewSet)
router.register(r'selections', SelectionViewSet)
router.register(r'messages', MessageViewSet)
