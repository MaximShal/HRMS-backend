from rest_framework import generics, viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from company.documentation.schemas_settings import user_doc
from hrms.decorators import viewset_swagger

from .models import Users
from .permissions import CustomPermission
from .serializers import RegistrationSerializer, UserSerializer


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
        serializer.save()

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
