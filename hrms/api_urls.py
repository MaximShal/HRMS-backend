from django.urls import include, path

urlpatterns = [
    path("", include("company.urls"), name="company")
]
