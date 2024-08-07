from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedUserAdminOrReadOnly(BasePermission):
    """Check Admin or Anonimus."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )


class IsAuthenticatedAuthorModeratorAdmin(BasePermission):
    """Check Moderator, Admin, Autor and Auten for GET."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
