from rest_framework import permissions

class IsCreatorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        elif view.action in ['create', 'retrieve', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated
        else:
            return False

    def has_object_permission(self, request, view, obj):

        # can all save ('GET', 'OPTIONS', 'HEAD')
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.creator == request.user or request.user.is_superuser:
            return True
        else:
            return False