from django.urls import path, include
from rest_framework.routers import DefaultRouter
from company.views import CompanyCreateView, UserViewSet


router = DefaultRouter()
router.register("", UserViewSet, basename="users")

urlpatterns = [
    path('company-create/', CompanyCreateView.as_view(), name='company-registration'),
    path("users/", include(router.urls)),
]
