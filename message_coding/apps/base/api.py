from django.contrib.auth import get_user_model
from rest_framework import routers, serializers, viewsets, permissions
from message_coding.apps.base import api_utils

from message_coding.apps.project import api as project_api
from message_coding.apps.dataset.api import urls as dataset_urls
from message_coding.apps.coding import api as coding_api


User = get_user_model()


# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff', 'projects',
                  'projects_owned', 'tasks_owned', 'tasks_assigned')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


router = api_utils.SuperRouter()
router.register('users', UserViewSet)
router.extend(project_api.router)
router.extend(dataset_urls.router)
router.extend(coding_api.router)

urlpatterns = router.urls
