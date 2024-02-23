from rest_framework import permissions

from .models import Permissions, UserRoleConnections


class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if user.is_staff:
            return True

        http_method = request.method.lower()
        view_name = view.__class__.__name__

        user_roles = UserRoleConnections.objects.filter(user_id=user.id)
        user_permissions = Permissions.objects.filter(
            rolepermissionconnections__role_id__in=user_roles.values_list('role_id', flat=True)
        ).distinct()

        if user_permissions.filter(operation__operation_name=http_method, resource__resource_name=view_name).exists():
            return True

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.company_id == user.company.id
