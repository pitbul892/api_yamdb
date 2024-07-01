from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.response import Response

User = get_user_model()


class AdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_admin or user.is_superuser
