from rest_framework import routers, serializers, permissions

class SuperRouterMixin(object):

    def extend(self, router):
        for prefix, viewset, base_name in router.registry:
            self.registry.append((prefix, viewset, base_name))

class SuperRouter(SuperRouterMixin, routers.DefaultRouter):
    pass

class SuperSimpleRouter(SuperRouterMixin, routers.SimpleRouter):
    pass


# http://stackoverflow.com/questions/24852555/how-to-exclude-parent-when-serializer-is-nested-when-using-django-rest-framework
class ExclusiveHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    """
    A HyperlinkedModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)
        # Instantiate the superclass normally
        super(ExclusiveHyperlinkedModelSerializer, self).__init__(*args, **kwargs)

        if fields:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        if exclude:
            # Drop fields that are specified in the `exclude` argument.
            excluded = set(exclude)
            for field_name in excluded:
                try:
                    self.fields.pop(field_name)
                except KeyError:
                    pass


class IsStaffOrOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.

        # User may be staff
        if request.user.is_staff:
            return True

        return obj.owner == request.user

