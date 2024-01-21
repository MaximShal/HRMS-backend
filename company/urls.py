from django.urls import include, path

from rest_framework.routers import DefaultRouter

from company.views import CompanyCreateView, UserViewSet


router = DefaultRouter()
router.register("user", UserViewSet, basename="user")

urlpatterns = [
    path('company-create/', CompanyCreateView.as_view(), name='company-registration'),
    path("", include(router.urls)),
]
