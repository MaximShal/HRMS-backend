from company.models import Operations, Permissions, Resources, RolePermissionConnections, Roles

from django.core.management.base import BaseCommand

# DRAFT!!!!!


class Command(BaseCommand):
    help = 'Load roles and permissions data into the database'

    def handle(self, *args, **options):
        # CLEAN TABLES    BE CAREFUL!!!!!
        Operations.objects.all().delete()
        Resources.objects.all().delete()
        Roles.objects.all().delete()
        Permissions.objects.all().delete()
        RolePermissionConnections.objects.all().delete()

        # Load operations
        operations_data = ['get', 'post', 'put', 'patch', 'delete']
        for operation_name in operations_data:
            Operations.objects.create(operation_name=operation_name)
            self.stdout.write(self.style.SUCCESS(f'Operation "{operation_name}" added successfully'))

        # Load resources
        resources_data = ['UserViewSet']
        for resource_name in resources_data:
            Resources.objects.create(resource_name=resource_name)
            self.stdout.write(self.style.SUCCESS(f'Resource "{resource_name}" added successfully'))

        # Load roles
        roles_data = ['companyowner', 'HR', 'Employee', 'Manager']
        for role_name in roles_data:
            Roles.objects.create(role_name=role_name)
            self.stdout.write(self.style.SUCCESS(f'Role "{role_name}" added successfully'))

        # Load permissions
        for operation_id in range(1, 6):
            for resource_id in range(1, 2):
                Permissions.objects.create(operation_id=operation_id, resource_id=resource_id)
                self.stdout.write(self.style.SUCCESS(f'Permission "{operations_data[operation_id-1]}" '
                                                     f'added successfully'))

        # Creations RolePermissionConnections
        hr_role = Roles.objects.get(role_name='HR')
        manager_role = Roles.objects.get(role_name='Manager')

        for operation_id in range(1, 6):
            RolePermissionConnections.objects.create(role_id=hr_role,
                                                     permission_id=Permissions.objects.get(operation_id=operation_id,
                                                                                           resource_id=1))
            RolePermissionConnections.objects.create(role_id=manager_role,
                                                     permission_id=Permissions.objects.get(operation_id=operation_id,
                                                                                           resource_id=1))

        self.stdout.write(self.style.SUCCESS('Role-Permission connections added successfully'))

# command - python manage.py load_data
