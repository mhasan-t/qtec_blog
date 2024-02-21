from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from .models import User


class AccountTests_Unauthorized(APITestCase):
    def test_create_account(self):
        url = reverse('user-list')

        data = {
            "username": "testuser",
            "email": "test@email.com",
            "full_name": "Test User",
            "password": "1234verystrongpassword!"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().full_name, 'Test User')

    def test_list_accounts(self):
        url = reverse('user-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_account(self):
        url = reverse('user-detail', kwargs={"pk": 1})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_account(self):
        url = reverse('user-detail', kwargs={"pk": 1})
        data = {
            "username": "changedUser",
        }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_account(self):
        url = reverse('user-detail', kwargs={"pk": 1})
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AccountTests_AuthorizedAsNormalUser(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.user = User.objects.create_user(
            id=1, username="niceuser", password="1234")
        self.user.user_type = 1
        self.user.save()

        token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token))

    def test_create_account(self):
        url = reverse('user-list')

        data = {
            "username": "testuser",
            "email": "test@email.com",
            "full_name": "Test User",
            "password": "1234verystrongpassword!"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get(
            username='testuser').full_name, 'Test User')

    def test_list_accounts(self):
        url = reverse('user-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_others_account(self):
        register_url = reverse('user-list')

        data = {
            "username": "testuser",
            "email": "test@email.com",
            "full_name": "Test User",
            "password": "1234verystrongpassword!"
        }
        response = self.client.post(register_url, data, format='json')

        url = reverse('user-detail', kwargs={"pk": response.data["id"]})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_own_account(self):
        url = reverse('user-detail', kwargs={"pk": self.user.id})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_others_account(self):
        register_url = reverse('user-list')

        other_data = {
            "username": "testuser",
            "email": "test@email.com",
            "full_name": "Test User",
            "password": "1234verystrongpassword!"
        }
        response = self.client.post(register_url, other_data, format='json')

        url = reverse('user-detail', kwargs={"pk": response.data["id"]})
        data = {
            "username": "changedUser",
        }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_own_account(self):
        url = reverse('user-detail', kwargs={"pk": self.user.id})
        data = {
            "username": "changedUser",
        }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_others_account(self):
        register_url = reverse('user-list')

        other_data = {
            "username": "testuser",
            "email": "test@email.com",
            "full_name": "Test User",
            "password": "1234verystrongpassword!"
        }
        response = self.client.post(register_url, other_data, format='json')

        url = reverse('user-detail', kwargs={"pk": response.data["id"]})
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_account(self):
        url = reverse('user-detail', kwargs={"pk": self.user.id})
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
