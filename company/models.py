from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Company(models.Model):            # Can create only First user, creating with registration
    company_name = models.CharField(max_length=255)

    def __str__(self):
        return self.company_name


class Users(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    address = models.TextField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')), blank=True)
    invited_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    # invited_by = models.ForeignKey('self', on_delete=models.CASCADE, default=1)
    department = models.TextField(max_length=100, blank=True)
    job_title = models.TextField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    objects = CustomUserManager()

    def delete(self, *args, **kwargs):
        # ReId of user if inviter was deleted
        if self.invited_by:
            invited_by_id = self.invited_by.id
            self.users_set.all().update(invited_by_id=invited_by_id)
        super().delete(*args, **kwargs)


class Roles(models.Model):        # Roles
    role_name = models.CharField(max_length=100)

    def __str__(self):
        return self.role_name


class Operations(models.Model):            # CRUD What operations can do user by his role
    operation_name = models.CharField(max_length=100)

    def __str__(self):
        return self.operation_name


class Resources(models.Model):            # Fields what user can change
    resource_name = models.CharField(max_length=100)

    def __str__(self):
        return self.resource_name


class Permissions(models.Model):          # Connect Operations and Resources
    operation = models.ForeignKey(Operations, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resources, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.operation.operation_name} - {self.resource.resource_name}"


class RolePermissionConnections(models.Model):
    role_id = models.ForeignKey(Roles, on_delete=models.CASCADE)
    permission_id = models.ForeignKey(Permissions, on_delete=models.CASCADE)


class UserRoleConnections(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    role_id = models.ForeignKey(Roles, on_delete=models.CASCADE)
