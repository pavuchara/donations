import pytest

from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from rest_framework import status

from donations_api.pytest_tests.user_constans import (
    IncorrectUserData,
    IncorrectPartialUpdateUser,
    CORRECT_USER_CREATE_DATA,
    CORRECT_USER_UPDARE_DATA,
    CORRECT_USER_PARTIAL_UPDARE_DATA,
    CORRECT_USER_TOKEN_OBTAIN_DATA,
)

User = get_user_model()


class TestUserCreation:
    """Логика завязанная на создание пользователя."""

    def test_user_creation_correct_data(self, anonymous_client, user_register_path):
        response = anonymous_client.post(user_register_path, CORRECT_USER_CREATE_DATA)
        assert response.status_code == status.HTTP_201_CREATED
        new_user = model_to_dict(User.objects.get(pk=response.data.get('id')))
        for key in CORRECT_USER_CREATE_DATA:
            if key != 'password':
                assert new_user[key] == CORRECT_USER_CREATE_DATA[key], (
                    'Данные после регистрации пользователя не совпадают.'
                )

    @pytest.mark.parametrize(
        'user_data',
        [
            IncorrectUserData.get_wrog_first_name(),
            IncorrectUserData.get_wrong_email(),
            IncorrectUserData.get_wrong_username(),
        ],
    )
    def test_user_creation_wrong_data(self, anonymous_client, user_register_path, user_data):
        response = anonymous_client.post(user_register_path, user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST, (
            'Кривые данные при регистрации вернули не 400.'
        )
        assert User.objects.count() == 0, 'Пользователь с кривыми данными создался'

    @pytest.mark.usefixtures('user_db')
    def test_user_creation_with_existing_data(self, anonymous_client, user_register_path):
        response = anonymous_client.post(user_register_path, CORRECT_USER_CREATE_DATA)
        assert response.status_code == status.HTTP_400_BAD_REQUEST, (
            'Юзер с существующими данными регистрируется, не должен.'
        )


class TestUserUpdates:
    """Логика завязанная на обновление данных пользователя."""

    def test_update_user_profile_owner_correct_data(self, auth_user_client, user_update_retrive_path):
        response = auth_user_client.put(user_update_retrive_path, CORRECT_USER_UPDARE_DATA)
        assert response.status_code == status.HTTP_200_OK
        updated_user = model_to_dict(User.objects.get(pk=response.data.get('id')))
        for key in CORRECT_USER_UPDARE_DATA:
            if key != 'password':
                assert updated_user[key] == CORRECT_USER_UPDARE_DATA[key], (
                    'Данные после обноелвени PUT пользователя не совпадают.'
                )

    @pytest.mark.parametrize(
        'user_data',
        [
            IncorrectUserData.get_wrog_first_name(),
            IncorrectUserData.get_wrong_email(),
            IncorrectUserData.get_wrong_username(),
        ],
    )
    def test_update_user_profile_owner_wrong_data(
        self, auth_user_client, user_update_retrive_path, user_data, user_db
    ):
        response = auth_user_client.put(user_update_retrive_path, user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        user_db.refresh_from_db()
        updated_user = model_to_dict(user_db)
        for key in CORRECT_USER_CREATE_DATA:
            if key != 'password':
                assert updated_user[key] == CORRECT_USER_CREATE_DATA[key], (
                    'Данные после обновления кривыми данными пользователя не совпадают.'
                )

    def test_patrial_update_user_profile_owner_correct_data(
        self, auth_user_client, user_update_retrive_path, user_db
    ):
        for k, v in CORRECT_USER_PARTIAL_UPDARE_DATA.items():
            response = auth_user_client.patch(user_update_retrive_path, {k: v})
            assert response.status_code == status.HTTP_200_OK
            user_db.refresh_from_db()
            updated_user = model_to_dict(user_db)
            assert updated_user[k] == CORRECT_USER_PARTIAL_UPDARE_DATA[k], (
                'Даннные после обновления PATCH пользователя не совпали.'
            )

    @pytest.mark.parametrize(
        'user_data, data_key',
        [
            (IncorrectPartialUpdateUser.get_wrog_first_name(), 'first_name'),
            (IncorrectPartialUpdateUser.get_wrong_email(), 'email'),
            (IncorrectPartialUpdateUser.get_wrong_username(), 'username'),
        ],
    )
    def test_patrial_update_user_profile_owner_wrong_data(
        self, auth_user_client, user_update_retrive_path, user_db, user_data, data_key
    ):
        response = auth_user_client.patch(user_update_retrive_path, user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        user_db.refresh_from_db()
        updated_user = model_to_dict(user_db)
        assert updated_user[data_key] == CORRECT_USER_CREATE_DATA[data_key], (
            'Даннные после обновления PATCH пользователя не совпали.'
        )

    def test_user_cant_edit_another_profile(
        self, auth_user_second_client, user_update_retrive_path, user_db
    ):
        response = auth_user_second_client.put(user_update_retrive_path, CORRECT_USER_UPDARE_DATA)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        user_db.refresh_from_db()
        updated_user = model_to_dict(user_db)
        for key in {k: v for k, v in CORRECT_USER_UPDARE_DATA.items() if k != 'password'}:
            assert updated_user[key] == CORRECT_USER_CREATE_DATA[key], (
                'Данные после обновления PUT профиля сторонним пользователем не совпадают.'
            )

    def test_user_cant_partial_edit_another_profile(
        self, auth_user_second_client, user_update_retrive_path, user_db
    ):
        for k, v in CORRECT_USER_UPDARE_DATA.items():
            response = auth_user_second_client.patch(user_update_retrive_path, {k: v})
            assert response.status_code == status.HTTP_403_FORBIDDEN
            user_db.refresh_from_db()
            updated_user = model_to_dict(user_db)
            for key in {k: v for k, v in CORRECT_USER_UPDARE_DATA.items() if k != 'password'}:
                assert updated_user[key] == CORRECT_USER_CREATE_DATA[key], (
                    'Данные после обновления PATCH профиля сторонним пользователем не совпадают.'
                )

    def test_anonymous_user_cant_update_profile(
        self, anonymous_client, user_update_retrive_path, user_db
    ):
        response = anonymous_client.put(user_update_retrive_path, CORRECT_USER_UPDARE_DATA)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        user_db.refresh_from_db()
        updated_user = model_to_dict(user_db)
        for key in CORRECT_USER_CREATE_DATA:
            if key != 'password':
                assert updated_user[key] == CORRECT_USER_CREATE_DATA[key], (
                    'Даннные после обновления PATCH анонима в профиле не совпали.'
                )

    def test_anonymous_user_cant_partial_update_profile(
        self, anonymous_client, user_update_retrive_path, user_db
    ):
        for k, v in CORRECT_USER_PARTIAL_UPDARE_DATA.items():
            response = anonymous_client.patch(user_update_retrive_path, {k: v})
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
            user_db.refresh_from_db()
            updated_user = model_to_dict(user_db)
            assert updated_user[k] == CORRECT_USER_CREATE_DATA[k], (
                'Даннные после обновления PATCH анонима в профиле не совпали.'
            )


class TestUserTokenLogic:
    """Логика завязанная на получение токена пользователем."""

    @pytest.mark.usefixtures('user_db')
    def test_user_can_obtain_refresh_token(
        self, anonymous_client, token_obtain_path, token_refresh_path
    ):
        response = anonymous_client.post(token_obtain_path, CORRECT_USER_TOKEN_OBTAIN_DATA)
        assert (
            response.status_code == status.HTTP_200_OK
            and 'refresh' in response.data
            and 'access' in response.data
            ), 'Не вышло получить токены'

        token = response.data.get('refresh')
        response = anonymous_client.post(token_refresh_path, {'refresh': token})

        assert (
            response.status_code == status.HTTP_200_OK
            and 'access' in response.data
        ), 'Не вышло получить access токен'
