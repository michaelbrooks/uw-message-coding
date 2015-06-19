from rest_framework import permissions

class IsAdminUserOrReadOnly(permissions.IsAuthenticated):
    """
    Only Admin User can modify it, otherwise read-only
    """

    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated():
            return False

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # The request user should be admin to get permissions on other methods
        return request.user and request.user.is_staff

class IsProjectMember(permissions.IsAuthenticated):
    """
    Object-level permission to only allow project members to access a project
    """

    def has_object_permission(self, request, view, obj):
        # staff always have permission
        if request.user and request.user.is_staff:
            return True

        # get the project for the object
        if hasattr(obj, 'project'):
            obj = obj.project

        if hasattr(obj, 'members'):
            return request.user in obj.members.all()

        raise Exception("Object %s has no project or members")

class IsProjectOwnerOrReadOnly(permissions.IsAuthenticated):
    """
    Object-level permission to only allow project owner to modify a project, otherwise members are read-only
    """

    def has_object_permission(self, request, view, obj):

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must be in the project owner.
        return (request.user and request.user.is_staff) or request.user == obj.owner

class IsTaskAssigner(permissions.IsAuthenticated):
    """
    Object-level permission to only allow task assigners to access a task
    """

    def has_object_permission(self, request, view, obj):
        # Instance must be in the project member.
        return (request.user and request.user.is_staff) or request.user in obj.assigned_coders.all()

class IsTaskOwnerOrReadOnly(permissions.IsAuthenticated):
    """
    Object-level permission to only allow task owner to modify a task, otherwise members are read-only
    """

    def has_object_permission(self, request, view, obj):

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True


        # Instance must be in the project owner.
        return (request.user and request.user.is_staff) or request.user == obj.owner
