from django.contrib import admin
from .models import (Company, Users, Roles, Operations, Resources, Permissions, RolePermissionConnections,
                     UserRoleConnections)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'address', 'phone_number', 'gender', 'invited_by',
                    'department', 'job_title', 'date_of_birth']
    list_filter = ['company', 'gender', 'date_of_birth']
    search_fields = ['username', 'email', 'first_name', 'last_name']


@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Operations)
class OperationsAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Resources)
class ResourcesAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Permissions)
class PermissionsAdmin(admin.ModelAdmin):
    list_display = ['operation', 'resource']


@admin.register(RolePermissionConnections)
class RolePermissionConnectionsAdmin(admin.ModelAdmin):
    list_display = ['role', 'permission']


@admin.register(UserRoleConnections)
class UserRoleConnectionsAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
