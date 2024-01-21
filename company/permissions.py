from django.urls import reverse
from rest_framework import permissions


class UsersPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            if request.path == reverse("user-list"):
                return request.user.is_staff
            return request.user.is_authenticated
        return False

    def has_object_permission(self, request, view, obj):
        return obj.pk == request.user.id or all([request.user.is_staff, obj.company.id == request.user.company.id])
