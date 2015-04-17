from message_coding.apps.coding import models
from rest_framework import routers, serializers, viewsets
from message_coding.apps.base import api_utils


class CodeSerializer(api_utils.ExclusiveModelSerializer):
    class Meta:
        model = models.Code
        fields = ('id', 'name', 'description', 'code_group')


class CodeGroupSerializer(api_utils.ExclusiveModelSerializer):
    class Meta:
        model = models.CodeGroup
        fields = ('id', 'name', 'description', 'codes', 'scheme')

    codes = CodeSerializer(many=True, exclude=('code_group',))


# Serializers define the API representation.
class SchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Scheme
        fields = ('id', 'name', 'description',
                  'created_at', 'owner', 'project', 'code_groups')

    code_groups = CodeGroupSerializer(many=True, exclude=('scheme',))


# ViewSets define the view behavior.
class SchemeViewSet(viewsets.ModelViewSet):
    queryset = models.Scheme.objects.all()
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
