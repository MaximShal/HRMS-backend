from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Company, Roles, Users, UserRoleConnections


class RegistrationSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ['email', 'password', 'password_confirm', 'company_name']

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
