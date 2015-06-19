from message_coding.apps.coding import models
from rest_framework import routers, serializers, viewsets
from message_coding.apps.base import api_utils, permissions, views


class OrderedListSerializer(serializers.ListSerializer):

    # def to_representation(self, data):
    #     """
    #     List of object instances -> List of dicts of primitive datatypes.
    #     """
    #     # Dealing with nested relationships, data can be a Manager,
    #     # so, first get a queryset from the Manager if needed
    #     iterable = data.all() if isinstance(data, (models.Manager, query.QuerySet)) else data
    #     return [
    #         self.child.to_representation(item) for item in iterable
    #     ]

    def update(self, instances, validated_data):
        # Maps for id->instance and id->data item.
        instance_map = {instance.pk: instance for instance in instances}

        # Perform creations and updates.
        return_instances = []
        id_set = set()
        for item in validated_data:
            instance = instance_map.get(item['id'], None)
            if instance is None:
                return_instances.append(self.child.create(item))
            else:
                return_instances.append(self.child.update(instance, item))
                id_set.add(instance.pk)

        # Perform deletions.
        for id, instance in instance_map.items():
            if id not in id_set:
                instance.delete()

        return return_instances


class CodeSerializer(api_utils.ExclusiveModelSerializer):
    class Meta:
        model = models.Code
        fields = ('id', 'name', 'description', 'code_group',)
        list_serializer_class = OrderedListSerializer


class CodeGroupSerializer(api_utils.ExclusiveModelSerializer):

    class Meta:
        model = models.CodeGroup
        fields = ('id', 'name', 'description', 'codes', 'scheme',)
        list_serializer_class = OrderedListSerializer

    codes = CodeSerializer(many=True)


# Serializers define the API representation.
class SchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Scheme
        fields = ('id', 'name', 'description',
                  'created_at', 'owner', 'project', 'code_groups', )
        read_only_fields = ('created_at', 'owner', )

    code_groups = CodeGroupSerializer(many=True)


# ViewSets define the view behavior.
class SchemeViewSet(views.OwnedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = (permissions.IsProjectMember,)
    queryset = models.Scheme.objects.all()
    lookup_url_kwarg = 'id'

    serializer_class = SchemeSerializer
    paginate_by = 50


class CodeGroupViewSet(viewsets.ModelViewSet):
    queryset = models.CodeGroup.objects.all()
    serializer_class = CodeGroupSerializer
    paginate_by = 50


class CodeViewSet(viewsets.ModelViewSet):
    queryset = models.Code.objects.all()
    serializer_class = CodeSerializer
    paginate_by = 50


# Routers provide an easy way of automatically determining the URL conf.
router = routers.SimpleRouter()
router.register(r'schemes', SchemeViewSet)
router.register(r'code_groups', CodeGroupViewSet)
router.register(r'codes', CodeViewSet)
