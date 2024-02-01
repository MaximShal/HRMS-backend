from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from .models import Company, Roles, UserRoleConnections, Users


class RegistrationSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    is_staff = serializers.BooleanField(default=True)

    class Meta:
        model = Users
        fields = ['email', 'password', 'password_confirm', 'company_name', 'is_staff']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Check the password")

        validate_password(data['password'])

        return data

    def create(self, validated_data):
        company_name = validated_data.pop('company_name')
        validated_data.pop('password_confirm')

        company = Company.objects.create(company_name=company_name)

        user = Users.objects.create_user(**validated_data)
        user.company = company
        user.save()

        # Назначение роли "companyowner"
        company_owner_role = Roles.objects.get(role_name='companyowner')
        UserRoleConnections.objects.create(user_id=user, role_id=company_owner_role)

        return user


class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)
    role = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError("Password and password confirmation do not match.")

        return data

    def create(self, validated_data):
        is_superuser = validated_data.pop('is_superuser', False)
        is_staff = validated_data.pop('is_staff', False)
        if is_superuser or is_staff:
            raise serializers.ValidationError("Permission Denied")

        validated_data.pop('password_confirm', None)
        role = validated_data.pop('role')
        if role is None:
            role = 'Employee'
        user = Users.objects.create_user(**validated_data)
        user.save()
        user_role = Roles.objects.get(role_name=role)
        UserRoleConnections.objects.create(user_id=user, role_id=user_role)
        return user
