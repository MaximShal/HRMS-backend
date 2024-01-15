from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from .serializers import LoginSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return Response({'token': token, 'message': 'Login successful'},
                        status=status.HTTP_200_OK)