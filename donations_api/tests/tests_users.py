from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory

from donations_api.views import UserCreateListView
from donations_api.tests.constans import (
    CORRECT_USER_CREATE_DATA,
    INCORRECT_USER_CREATE_DATA,
)


User = get_user_model()


class UserCreateTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_create_view = UserCreateListView.as_view()

    def test_user_creations(self):
        request = self.factory.post('users/', CORRECT_USER_CREATE_DATA)
        response = self.user_create_view(request)

        with self.subTest(name='Response test'):
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.data['email'], CORRECT_USER_CREATE_DATA['email'])

        with self.subTest(name='DB test'):
            self.assertEqual(User.objects.count(), 1)
            user = User.objects.get(pk=response.data['id'])
            self.assertEqual(user.email, CORRECT_USER_CREATE_DATA['email'])

    def test_user_creation_with_wrong_data(self):
        request = self.factory.post('users/', INCORRECT_USER_CREATE_DATA)
        response = self.user_create_view(request)
        self.assertEqual(response.status_code, 400)

    def test_user_creation_with_existing_email(self):
        request = self.factory.post('users/', CORRECT_USER_CREATE_DATA)
        respose = self.user_create_view(request)
        self.assertEqual(respose.status_code, 201)
        respose = self.user_create_view(request)
        self.assertEqual(respose.status_code, 400)
