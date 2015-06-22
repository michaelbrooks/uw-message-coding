from rest_framework import routers, pagination
from rest_framework.response import Response

class SuperRouterMixin(object):

    def extend(self, router):
        for prefix, viewset, base_name in router.registry:
            self.registry.append((prefix, viewset, base_name))

class SuperRouter(SuperRouterMixin, routers.DefaultRouter):
    pass

class SuperSimpleRouter(SuperRouterMixin, routers.SimpleRouter):
    pass



class CustomPagination(pagination.PageNumberPagination):
    """API pagination serializer that adds num_pages and per_page"""
    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'page_count': self.page.paginator.num_pages,
            'per_page': self.page.paginator.per_page,
            'count': self.page.paginator.count,
            'results': data
        })
