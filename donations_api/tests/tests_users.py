from django.test import TestCase
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient

from donations_api.views import UserCreateListView
from donations_api.tests.user_constans import (
    CORRECT_USER_CREATE_DATA,
    INCORRECT_USER_CREATE_DATA,
    CORRECT_USER_PARTIAL_UPDARE_DATA,
    CORRECT_USER_UPDARE_DATA,
    INCORRECT_USER_UPDARE_DATA,
    INCORRECT_USER_PARTIAL_UPDARE_DATA,
    CORRECT_USER_TOKEN_OBTAIN_DATA,
)


User = get_user_model()


class UserCreateTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_create_view = UserCreateListView.as_view()
        self.user_create_path = '/api/v1/users/'

    def test_user_creations(self):
        """Создание пользователя с корректными данными."""
        request = self.factory.post(self.user_create_path, CORRECT_USER_CREATE_DATA)
        response = self.user_create_view(request)

        with self.subTest(name='Response test'):
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data['email'], CORRECT_USER_CREATE_DATA['email'])

        with self.subTest(name='DB test'):
            self.assertEqual(User.objects.count(), 1)
            user = User.objects.get(pk=response.data['id'])
            self.assertEqual(user.email, CORRECT_USER_CREATE_DATA['email'])

    def test_user_creation_with_wrong_data(self):
        """Создание пользователя с некорректными данными."""
        request = self.factory.post(self.user_create_path, INCORRECT_USER_CREATE_DATA)
        response = self.user_create_view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_creation_with_existing_data(self):
        """Создание пользователя с корректными данными, но уже существующими."""
        request = self.factory.post(self.user_create_path, CORRECT_USER_CREATE_DATA)
        respose = self.user_create_view(request)
        self.assertEqual(respose.status_code, status.HTTP_201_CREATED)
        respose = self.user_create_view(request)
        self.assertEqual(respose.status_code, status.HTTP_400_BAD_REQUEST)


class UserUpdateTestCase(TestCase):

    def setUp(self):
        self.user_db = User.objects.create(**{k: v for k, v in CORRECT_USER_CREATE_DATA.items() if k != 'password'})
        self.user_db.set_password(CORRECT_USER_CREATE_DATA['password'])
        self.user_db.save()
        self.user_client = APIClient()
        self.user_client.force_authenticate(self.user_db)
        self.user_update_path = f'/api/v1/users/{self.user_db.pk}/'

    def test_update_user(self):
        """Тесты PUT обновления пользователя
           users_info: tuple
               user_data: Данные для запроса на обновление,
               response_status: ожидаемый статус,
               name: Для subTest и удобства отладки,
               expected: Ожидаеммые данные после запроса.
        """
        users_info = (
            (CORRECT_USER_UPDARE_DATA, status.HTTP_200_OK, "correct_data", CORRECT_USER_UPDARE_DATA),
            (INCORRECT_USER_UPDARE_DATA, status.HTTP_400_BAD_REQUEST, "incorrect_data", CORRECT_USER_UPDARE_DATA),
        )

        for user_data, response_status, name, expected in users_info:
            with self.subTest(name=name):
                response = self.user_client.put(self.user_update_path, user_data)
                self.assertEqual(response.status_code, response_status)
                self.user_db.refresh_from_db()
                self.assertEqual(self.user_db.first_name, expected['first_name'])

    def test_partial_update(self):
        """Тесты PATCH обновления пользователя
           users_info: tuple
               user_data: Данные для запроса на обновление,
               response_status: ожидаемый статус,
               name: Для subTest и удобства отладки,
               expected: Ожидаеммые данные после запроса.
        """
        users_info = (
            (CORRECT_USER_PARTIAL_UPDARE_DATA, status.HTTP_200_OK,
             "correct_data", CORRECT_USER_PARTIAL_UPDARE_DATA),
            (INCORRECT_USER_PARTIAL_UPDARE_DATA, status.HTTP_400_BAD_REQUEST,
             "incorrect_data", CORRECT_USER_PARTIAL_UPDARE_DATA),
        )
        for user_data, response_status, name, expected in users_info:
            with self.subTest(name=name):
                for k, v in user_data.items():
                    response = self.user_client.patch(self.user_update_path, {k: v})
                    self.assertEqual(response.status_code, response_status)
                    self.user_db.refresh_from_db()
                    self.assertEqual(model_to_dict(self.user_db)[k], expected[k])


class UserTokenTestCase(TestCase):

    def setUp(self):
        self.user_db = User.objects.create(**{k: v for k, v in CORRECT_USER_CREATE_DATA.items() if k != 'password'})
        self.user_db.set_password(CORRECT_USER_CREATE_DATA['password'])
        self.user_db.save()
        self.user_client = APIClient()
        self.user_client.force_authenticate(self.user_db)
        self.token_obtain = '/api/v1/token/'
        self.token_refresh = '/api/v1/token/refresh/'

    def test_tocken_obtain_refresh_with_correct_data(self):
        """Получение и обновление токена с корректными данными."""
        with self.subTest(name='Obtain tocken'):
            response = self.user_client.post(self.token_obtain, CORRECT_USER_TOKEN_OBTAIN_DATA)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('refresh', response.data)
            self.assertIn('access', response.data)
            token = response.data['refresh']

        with self.subTest(name='Refresh token'):
            response = self.user_client.post(self.token_refresh, {'refresh': token})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('access', response.data)
