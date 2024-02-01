from django.contrib import admin

from .models import (Company, Operations, Permissions, Resources, RolePermissionConnections, Roles,
                     UserRoleConnections, Users,)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_name']


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'address', 'phone_number', 'gender', 'invited_by',
                    'department', 'job_title', 'date_of_birth']
    list_filter = ['company', 'gender', 'date_of_birth']
    search_fields = ['username', 'email', 'first_name', 'last_name']


@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    list_display = ['role_name']


@admin.register(Operations)
class OperationsAdmin(admin.ModelAdmin):
    list_display = ['operation_name']


@admin.register(Resources)
class ResourcesAdmin(admin.ModelAdmin):
    list_display = ['resource_name']


@admin.register(Permissions)
class PermissionsAdmin(admin.ModelAdmin):
    list_display = ['operation', 'resource']


@admin.register(RolePermissionConnections)
class RolePermissionConnectionsAdmin(admin.ModelAdmin):
    list_display = ['role_id', 'permission_id']


@admin.register(UserRoleConnections)
class UserRoleConnectionsAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'role_id']
