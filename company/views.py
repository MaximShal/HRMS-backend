from uuid import uuid4

from company.documentation.schemas_settings import user_doc
from company.tasks import send_invitation_email_task, send_password_reset_email_task

from hrms.decorators import viewset_swagger

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Users
from .permissions import CustomPermission
from .serializers import InviteRegistrationSerializer, RegistrationSerializer, UserSerializer, \
    PasswordResetConfirmSerializer, PasswordResetRequestSerializer

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import generics, status
from rest_framework.response import Response


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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(company_id=request.user.company.id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        current_user = self.request.user if self.request.user.is_authenticated else None

        serializer.validated_data['invited_by'] = current_user
        serializer.validated_data['company'] = current_user.company

        invite_token = uuid4()
        serializer.validated_data['invite_token'] = invite_token
        serializer.save()
        send_invitation_email_task.delay(serializer.instance.id)    # Celery task


class InviteRegistrationView(generics.CreateAPIView):
    serializer_class = InviteRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        invite_token = serializer.validated_data.get('invite_token')
        user = Users.objects.filter(invite_token=invite_token).first()
        if not user:
            return Response({"detail": "Token does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()

        return Response({"detail": "Registration successful"}, status=status.HTTP_201_CREATED)


class PasswordResetRequestView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if not email:
            return Response({'detail': 'Email field is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            return Response({'detail': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Token generation to reset the pass
        token_generator = PasswordResetTokenGenerator()
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        reset_link = f"https://yourwebsite.com/reset-password/{uidb64}/{token}/"
        send_password_reset_email_task.delay(email, reset_link)   # CELERY TASK

        return Response({'detail': 'Email sent'}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetConfirmSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.data

            try:
                uid = urlsafe_base64_decode(data['uidb64']).decode()
                user = Users.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
                user = None

            if user and PasswordResetTokenGenerator().check_token(user, data['token']):
                user.set_password(data['new_password'])
                user.save()
                return Response({'detail': 'Password reset successfully'}, status=status.HTTP_200_OK)
            return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
