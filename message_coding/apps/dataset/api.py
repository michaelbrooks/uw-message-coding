from apps.dataset.models import Dataset, Selection, Message
from rest_framework import routers, serializers, viewsets
from base.views import OwnedViewSetMixin
import json


# Serializers define the API representation.
class DatasetSerializer(serializers.ModelSerializer):
    min_time = serializers.DateTimeField()
    max_time = serializers.DateTimeField()
    class Meta:
        model = Dataset
        fields = ('id', 'name', 'description', 'slug', 'created_at',
                  'owner', 'projects', 'min_time', 'max_time')
        read_only_fields = ('created_at',)


class TypedBlobField(serializers.Field):
    """
    This field translates binary descriptions in the database for the REST api.
    It uses a second field on the model, the 'type' field,
    to determine how to encode and decode the blob field.
    """

    def __init__(self,
                 type_field='type',
                 default_type='json',
                 **kwargs):
        self.type_field = type_field
        self.default_type = default_type
        self.value_type = default_type

        super(TypedBlobField, self).__init__(**kwargs)

    def to_representation(self, value):
        if self.value_type == 'json':
            return json.loads(value)
        else:
            return value

    def to_internal_value(self, data):
        if self.value_type == 'json':
            return json.dumps(data)
        else:
            return data

    def get_value(self, dictionary):
        self.value_type = dictionary.get(self.type_field, self.default_type)
        return super(TypedBlobField, self).get_value(dictionary)

    def get_attribute(self, instance):
        self.value_type = getattr(instance, self.type_field, self.default_type)
        return super(TypedBlobField, self).get_attribute(instance)


class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ('id', 'created_at', 'owner', 'dataset', 'type', 'selection', 'size')
        read_only_fields = ('created_at', 'owner', 'size',)

    selection = TypedBlobField(type_field='type', default_type='json')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'sender', 'time', 'text', 'dataset')


# ViewSets define the view behavior.
class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    paginate_by = 10


class SelectionViewSet(OwnedViewSetMixin, viewsets.ModelViewSet):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    paginate_by = 10


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    paginate_by = 10

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
