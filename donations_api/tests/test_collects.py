from datetime import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.test import APIClient

from collective_donations.models import Collect
from donations_api.tests.user_constans import (
    CORRECT_USER_CREATE_DATA,
    CORRECT_SECOND_USER_CREATE_DATA,
)
from donations_api.tests.collects_constants import (
    CORRECT_COLLECT_CREATE_DATA,
    CORRECT_UPDARE_DATA,
    Incorrect_collect_create_data,
)

User = get_user_model()


class CollectsCreateTestCase(TestCase):
    collect_create_path = '/api/v1/collects/'

    def setUp(self):
        self.user_db = User.objects.create(**{k: v for k, v in CORRECT_USER_CREATE_DATA.items() if k != 'password'})
        self.user_db.set_password(CORRECT_USER_CREATE_DATA['password'])
        self.user_db.save()
        self.user_client = APIClient()
        self.user_client.force_authenticate(self.user_db)
        self.anon_user = APIClient()

    def test_auth_user_correct_data_create_collect(self):
        response = self.user_client.post(self.collect_create_path, CORRECT_COLLECT_CREATE_DATA)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        collect = model_to_dict(Collect.objects.get(pk=response.data.get('id')))
        collect['end_datetime'] = datetime.strftime(collect['end_datetime'], '%Y-%m-%d')
        for key in CORRECT_COLLECT_CREATE_DATA:
            self.assertEqual(collect[key], CORRECT_COLLECT_CREATE_DATA[key])

    def test_auth_user_incorrect_data_create_collect(self):
        INCORRECT_DATA = (
            (Incorrect_collect_create_data.get_incorrect_end_datetime(), 'incorrect_end_datetime'),
            (Incorrect_collect_create_data.get_incorrect_slug(), 'incorrect_slug'),
            (Incorrect_collect_create_data.get_incorrect_target_amount(), 'incorrect_target_amount')
        )

        for incorrect_data, name in INCORRECT_DATA:
            with self.subTest(name=name):
                response = self.user_client.post(self.collect_create_path, incorrect_data)
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(Collect.objects.count(), 0)

    def test_not_auth_user_cant_create_collect(self):
        request = self.anon_user.post(self.collect_create_path, CORRECT_COLLECT_CREATE_DATA)
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Collect.objects.count(), 0)


class CollectsUpdateTestCase(TestCase):

    def setUp(self):
        # Автор.
        self.user_author_db = User.objects.create(
            **{k: v for k, v in CORRECT_USER_CREATE_DATA.items() if k != 'password'}
        )
        self.user_author_db.set_password(CORRECT_USER_CREATE_DATA['password'])
        self.user_author_db.save()
        self.user_author_client = APIClient()
        self.user_author_client.force_authenticate(self.user_author_db)
        # Не автор.
        self.user_not_author_db = User.objects.create(
            **{k: v for k, v in CORRECT_SECOND_USER_CREATE_DATA.items() if k != 'password'}
        )
        self.user_not_author_db.set_password(CORRECT_SECOND_USER_CREATE_DATA['password'])
        self.user_not_author_db.save()
        self.user_not_author_client = APIClient()
        self.user_not_author_client.force_authenticate(self.user_not_author_db)
        # Аноним.
        self.anon_user = APIClient()
        # Сбор
        self.collect = Collect.objects.create(**CORRECT_COLLECT_CREATE_DATA, author=self.user_author_db)
        self.collect_path = f'/api/v1/collects/{self.collect.pk}/'

    def test_partial_update_collect_auth_user_correct_data(self):
        for k, v in CORRECT_UPDARE_DATA.items():
            with self.subTest(name=f'correct {k}'):
                response = self.user_author_client.patch(self.collect_path, {k: v})
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.collect.refresh_from_db()
                collect = model_to_dict(Collect.objects.get(pk=response.data.get('id')))
                collect['end_datetime'] = datetime.strftime(collect['end_datetime'], '%Y-%m-%d')
                self.assertEqual(collect[k], CORRECT_UPDARE_DATA[k])

    def test_update_collect_auth_user_correct_data(self):
        response = self.user_author_client.put(self.collect_path, CORRECT_UPDARE_DATA)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.collect.refresh_from_db()
        collect = model_to_dict(Collect.objects.get(pk=self.collect.pk))
        collect['end_datetime'] = datetime.strftime(collect['end_datetime'], '%Y-%m-%d')
        for key in CORRECT_UPDARE_DATA:
            self.assertEqual(collect[key], CORRECT_UPDARE_DATA[key])

    def test_not_author_or_anonymous_cant_edit_collect(self):
        users_data = (
            (self.user_not_author_client, status.HTTP_403_FORBIDDEN),
            (self.anon_user, status.HTTP_401_UNAUTHORIZED)
        )

        for user_client, response_status in users_data:
            with self.subTest(name=f'{user_client}'):
                response = user_client.patch(self.collect_path, {'slug': 'string2'})
                self.assertEqual(response.status_code, response_status)
                self.collect.refresh_from_db()
                self.assertEqual(self.collect.slug, CORRECT_COLLECT_CREATE_DATA['slug'])
