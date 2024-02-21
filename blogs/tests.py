from django.test import TestCase, Client

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import User
from .models import Blog, Category, Post


class BlogTests_Unauthorized(APITestCase):
    def test_create_blog(self):
        url = reverse('blog-list')

        data = {
            "title": "This blog is about cats",
            "description": "Very epic cats here",
            "category_id": 1,
            "banner": "cats.png"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_blogs(self):
        url = reverse('blog-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_blog(self):
        url = reverse('blog-detail', kwargs={"pk": 1})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_blog(self):
        url = reverse('blog-detail', kwargs={"pk": 1})
        data = {
            "title": "Now it's about dogs",
        }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_blog(self):
        url = reverse('blog-detail', kwargs={"pk": 1})
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BlogTests_AuthorizedAsAuthor(APITestCase):
    def create_blog_response(self):
        category_obj = Category.objects.create(
            id=1, title="Pets", description="pets corner")

        blog_url = reverse('blog-list')
        blog_response = None
        with open('blogs/test_data/cat.jpg', 'rb') as img:
            data = {
                "title": "This blog is about cats",
                "description": "Very epic cats here",
                "category_id": category_obj.id,
                "banner": img
            }
            blog_response = self.client.post(
                blog_url, data, format='multipart')

        return blog_response

    def setUp(self) -> None:
        super().setUp()
        self.user = User.objects.create_user(
            id=1, username="niceuser", password="1234")
        self.user.user_type = 1
        self.user.save()

        token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token))

    def test_create_blog(self):
        category_obj = Category.objects.create(
            id=1, title="Pets", description="pets corner")

        url = reverse('blog-list')

        with open('blogs/test_data/cat.jpg', 'rb') as img:
            data = {
                "title": "This blog is about cats",
                "description": "Very epic cats here",
                "category_id": category_obj.id,
                "banner": img
            }
            response = self.client.post(url, data, format='multipart')

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_blogs(self):
        url = reverse('blog-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_blog(self):
        blog_response = self.create_blog_response()

        url = reverse('blog-detail', kwargs={"pk": blog_response.data["id"]})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_blog(self):
        blog_response = self.create_blog_response()

        url = reverse('blog-detail', kwargs={"pk": blog_response.data["id"]})
        data = {
            "title": "Now it's about dogs",
        }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_blog(self):
        blog_response = self.create_blog_response()

        url = reverse('blog-detail', kwargs={"pk": blog_response.data["id"]})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class BlogTests_AuthorizedAsNormalUser(APITestCase):
    def create_blog_response_as_author(self):
        # new api client because the self.client is configured with normal user auth
        client = APIClient()

        # author user object
        user = User.objects.create_user(
            id=99, username="niceauthor", password="1234")
        user.user_type = 1
        user.save()

        token = AccessToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token))

        # create category and blog
        category_obj = Category.objects.create(
            id=1, title="Pets", description="pets corner")

        blog_url = reverse('blog-list')
        blog_response = None
        with open('blogs/test_data/cat.jpg', 'rb') as img:
            data = {
                "title": "This blog is about cats",
                "description": "Very epic cats here",
                "category_id": category_obj.id,
                "banner": img
            }
            blog_response = client.post(
                blog_url, data, format='multipart')

        return blog_response

    def setUp(self) -> None:
        super().setUp()
        self.user = User.objects.create_user(
            id=1, username="niceuser", password="1234")
        self.user.user_type = 2
        self.user.save()

        token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token))

    def test_create_blog(self):
        category_obj = Category.objects.create(
            id=1, title="Pets", description="pets corner")

        url = reverse('blog-list')

        with open('blogs/test_data/cat.jpg', 'rb') as img:
            data = {
                "title": "This blog is about cats",
                "description": "Very epic cats here",
                "category_id": category_obj.id,
                "banner": img
            }
            response = self.client.post(url, data, format='multipart')

            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_blogs(self):
        url = reverse('blog-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_blog(self):
        blog_response = self.create_blog_response_as_author()

        url = reverse('blog-detail', kwargs={"pk": blog_response.data["id"]})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_blog(self):
        blog_response = self.create_blog_response_as_author()

        url = reverse('blog-detail', kwargs={"pk": blog_response.data["id"]})
        data = {
            "title": "Now it's about dogs",
        }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_blog(self):
        blog_response = self.create_blog_response_as_author()

        url = reverse('blog-detail', kwargs={"pk": blog_response.data["id"]})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
