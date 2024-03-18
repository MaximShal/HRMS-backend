from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import InviteRegistrationView, RegistrationView, UserProfileAPIView, UserViewSet, PasswordResetRequestView, \
    PasswordResetConfirmView

router = DefaultRouter()
router.register("user", UserViewSet, basename="user")


urlpatterns = [
    path('register/', RegistrationView.as_view(), name='user-registration'),
    path("", include(router.urls)),
    path("profile/", UserProfileAPIView.as_view()),
    path('invite-registration/', InviteRegistrationView.as_view(), name='invite-registration'),
    path('reset_password/', PasswordResetRequestView.as_view(), name='reset-password'),
    path('password_reset_confirm/', PasswordResetConfirmView.as_view(), name='reset-pass-confirm'),
]
