from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from company.models import Company, Roles, UserRoleConnections, Users


class CompanyCreateSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ['email', 'password', 'password_confirm', 'company_name']

    def validate(self, data):
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError("Check the password")

        validate_password(data['password'])

        return data

    def create(self, validated_data):
        company_name = validated_data.pop('company_name')
        company = Company.objects.create(name=company_name)

        user = Users.objects.create_user(**validated_data)
        user.company = company
        user.is_staff = True
        user.save()

        # Назначение роли "companyowner"
        company_owner_role, flag = Roles.objects.get_or_create(name='companyowner')
        UserRoleConnections.objects.create(user_id=user.id, role_id=company_owner_role.id)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}
