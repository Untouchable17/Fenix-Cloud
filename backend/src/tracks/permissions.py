from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated and obj.user == request.user
        )