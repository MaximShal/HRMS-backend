from django.test import TestCase
from django.urls import reverse
from random import randint
from rest_framework import status
from rest_framework.test import APIClient
from company.models import Users, Company


class CompanyCreateTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.company_acc = self._generate_data(5)

    @staticmethod
    def _generate_data(count: int = 1) -> list[dict]:
        return [
            {"email": f"user{i}@example.com",
             "password": "string123",
             "password_confirm": "string123",
             "company_name": "TestCompany"}
            for i in range(count)]

    def test_true_creation(self):
        for new_company in self.company_acc:
            response = self.client.post(reverse('company-registration'), new_company, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Response status invalid')
            self.assertTrue(Users.objects.filter(email=new_company.get('email')).exists(), 'Obj doesn`t exist')

    def test_false_creation(self):
        company = self.company_acc.pop(0)
        company["password_confirm"] += '0'
        response = self.client.post(reverse('company-registration'), company, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'Response status invalid')
        self.assertFalse(Users.objects.filter(email=company.get('email')).exists(), 'Obj exists')
        company.pop("password_confirm")
        response = self.client.post(reverse('company-registration'), company, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'Response status invalid')
        self.assertFalse(Users.objects.filter(email=company.get('email')).exists(), 'Obj exists')

        for i, el in enumerate(['@', '.']):
            company = self.company_acc.pop(i)
            company['email'] = ''.join(company['email'].split(el))
            response = self.client.post(reverse('company-registration'), company, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'Response status invalid')
            self.assertFalse(Users.objects.filter(email=company.get('email')).exists(), 'Obj exists')


class UserViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        company = Company.objects.create(name='TheBestCompany')
        self.client.force_authenticate(
            user=Users.objects.create_user(email="company_admin@example.com",
                                           password="examplepass1221",
                                           is_staff=True,
                                           company_id=company.id)
        )
        self.company_users = self._generate_users(company.id, 3)
        company = Company.objects.create(name='TheNormalCompany')
        self.another_company_users = self._generate_users(company.id, 2)

    @staticmethod
    def _generate_users(company_id: int, count: int = 1) -> list[Users]:
        return [Users.objects.create_user(email=f"test{randint(1000, 9999)}@example.com",
                                          password="examplepass1221",
                                          company_id=company_id) for _ in range(count)]

    def test_list_with_permissions(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(map(lambda x: x['company'] == self.company_users[0].company.id, response.data)))

        client = APIClient()
        response = client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client.force_authenticate(self.company_users[0])
        response = client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.company_users[0].is_staff = True
        response = client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(map(lambda x: x['company'] == self.company_users[0].company.id, response.data)))
