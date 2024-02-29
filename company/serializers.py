import random
import string

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
    role = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, required=False)

    return_fields = (
        'id', 'email', 'last_login', 'first_name', 'last_name', 'date_joined', 'phone_number', 'gender', 'department',
        'job_title', 'date_of_birth', 'address', 'company', 'invited_by'
    )

    class Meta:
        model = Users
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Delete fields in response except return_fields
        return {key: value for key, value in data.items() if key in self.return_fields}

    def create(self, validated_data):
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        is_superuser = validated_data.pop('is_superuser', False)
        is_staff = validated_data.pop('is_staff', False)
        if is_superuser or is_staff:
            raise serializers.ValidationError("Permission Denied")

        role = validated_data.pop('role')
        if role is None:
            role = 'Employee'
        user = Users.objects.create_user(**validated_data)

        user.set_password(password)
        user.save()
        user_role = Roles.objects.get(role_name=role)
        UserRoleConnections.objects.create(user_id=user, role_id=user_role)
        return user


class InviteRegistrationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)
    invite_token = serializers.UUIDField()

    class Meta:
        model = Users
        fields = ('password', 'password_confirm', 'invite_token')

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Check the password")

        validate_password(data['password'])

        return data

    def create(self, validated_data):
        user = Users.objects.get(invite_token=validated_data.pop('invite_token'))
        user.set_password(validated_data.pop('password'))
        user.save()
        user.invite_token = None
        user.save()
        return user
