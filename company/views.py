from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import CompanyCreateSerializer, UserSerializer
from .models import Users


class CompanyCreateView(generics.CreateAPIView):
    serializer_class = CompanyCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'User was successfully created'},
                        status=status.HTTP_201_CREATED, headers=headers)


class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [CanInteractWithUserAPI]
