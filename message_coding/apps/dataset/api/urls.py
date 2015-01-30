from rest_framework import routers
from apps.dataset.api import views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.SimpleRouter()
router.register(r'datasets', views.DatasetViewSet)
router.register(r'selections', views.SelectionViewSet)
router.register(r'messages', views.MessageViewSet)
