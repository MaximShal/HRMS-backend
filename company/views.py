from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from company.serializers import CompanyCreateSerializer, UserSerializer
from company.models import Users
from company.permissions import UsersPermissions


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
    permission_classes = [UsersPermissions]

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK,
                        data=self.get_serializer(self.queryset.filter(company_id=request.user.company), many=True).data)

