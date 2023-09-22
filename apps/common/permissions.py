from django.db.models import Q
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from datetime import datetime, timezone
from rest_framework import permissions
from apps.common.roles import RoleName


class StudentOrAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        roles = request.user.role.all().values_list('name', flat=True)
        if RoleName.STUDENT or RoleName.ADMIN in roles:
            return True
        return request.method in permissions.SAFE_METHODS
