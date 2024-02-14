from uuid import uuid4

from rest_framework import generics, viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from company.documentation.schemas_settings import user_doc

from hrms.decorators import viewset_swagger

from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

from .models import Users
from .permissions import CustomPermission
from .serializers import RegistrationSerializer, UserSerializer, InviteRegistrationSerializer


class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'User was successfully created'},
                        status=status.HTTP_201_CREATED, headers=headers)


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@viewset_swagger("user", additional_data=user_doc)
class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [CustomPermission]

    def perform_create(self, serializer):
        current_user = self.request.user if self.request.user.is_authenticated else None

        serializer.validated_data['invited_by'] = current_user
        serializer.validated_data['company'] = current_user.company

        invite_token = uuid4()
        serializer.validated_data['invite_token'] = invite_token
        serializer.save()

        self.send_invitation_email(serializer.instance)

    def send_invitation_email(self, user):
        registration_url = reverse('invite-registration') + f'?token={user.invite_token}'
        # message = f"Limk to complete the registration: {settings.BASE_URL}{registration_url}"
        message = f"Limk to complete the registration: {registration_url}"
        send_mail(
            'Registration invite',
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(company_id=request.user.company.id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.company_id != request.user.company.id:
            return Response({"detail": "Permission denied."}, status=403)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.company_id != request.user.company.id:
            return Response({"detail": "Permission denied."}, status=403)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.company_id != request.user.company.id:
            return Response({"detail": "Permission denied."}, status=403)
        self.perform_destroy(instance)
        return Response(status=204)


class InviteRegistrationView(generics.CreateAPIView):
    serializer_class = InviteRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({"detail": "Registration successful"}, status=status.HTTP_201_CREATED)
