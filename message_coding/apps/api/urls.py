from rest_framework import routers

from message_coding.apps.api import api_utils
from message_coding.apps.api import views

router = api_utils.SuperRouter()
router.register('users', views.UserViewSet)

project = routers.SimpleRouter()
project.register(r'projects', views.ProjectViewSet)
project.register(r'tasks', views.TaskViewSet)
project.register(r'code_instances', views.CodeInstanceViewSet)
router.extend(project)

dataset = routers.SimpleRouter()
dataset.register(r'datasets', views.DatasetViewSet)
dataset.register(r'messages', views.MessageViewSet)
router.extend(dataset)

coding = routers.SimpleRouter()
coding.register(r'schemes', views.SchemeViewSet)
coding.register(r'code_groups', views.CodeGroupViewSet)
coding.register(r'codes', views.CodeViewSet)
router.extend(coding)

urlpatterns = router.urls
