from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

User = get_user_model()


class RoleAdminOrSuperuserOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            user = User.objects.get(pk=request.user.id)
        except Exception:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        else:
            return user.is_admin() or user.is_superuser