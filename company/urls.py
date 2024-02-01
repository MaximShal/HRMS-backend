from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import RegistrationView, UserProfileAPIView, UserViewSet

router = DefaultRouter()
router.register("user", UserViewSet, basename="user")


urlpatterns = [
    path('register/', RegistrationView.as_view(), name='user-registration'),
    path("", include(router.urls)),
    path("profile/", UserProfileAPIView.as_view())
]
