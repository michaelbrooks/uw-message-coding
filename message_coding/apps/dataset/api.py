from apps.dataset.models import Dataset, Selection, Message
from rest_framework import routers, serializers, viewsets
import json

# Serializers define the API representation.
class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ('id', 'name', 'description', 'slug', 'created_at',
                  'owner', 'projects')
        read_only_fields = ('created_at',)


class JSONBinaryField(serializers.Field):
    def to_internal_value(self, obj):
        return json.dumps(obj)

    def to_representation(self, value):
        return json.loads(value)


class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ('id', 'created_at', 'owner', 'dataset', 'type', 'selection', 'size')
        read_only_fields = ('created_at', 'owner', 'size',)

    selection = JSONBinaryField

class MessageSerializer(serializers.ModelSerializer):
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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    paginate_by = 1

    def get_queryset(self):
        queryset = Message.objects.all()

        dataset_id = self.request.query_params.get('dataset_id', None)
        if dataset_id is not None:
            queryset = queryset.filter(dataset_id=dataset_id)

        return queryset

# Routers provide an easy way of automatically determining the URL conf.
router = routers.SimpleRouter()
router.register(r'datasets', DatasetViewSet)
router.register(r'selections', SelectionViewSet)
router.register(r'messages', MessageViewSet)
