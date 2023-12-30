from django.db import models
from django.contrib.auth.models import AbstractUser


class Company(AbstractUser):
    name = models.CharField(max_length=255)
    address = models.TextField(max_length=255)
    phone_number = models.CharField(max_length=20)
    industry = models.CharField(max_length=100)
