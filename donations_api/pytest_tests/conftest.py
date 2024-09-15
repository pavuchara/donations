import pytest
from rest_framework.test import APIClient

from donations_api.pytest_tests.user_constans import (
    CORRECT_USER_CREATE_DATA,
    CORRECT_SECOND_USER_CREATE_DATA,
)


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def user_db(django_user_model):
    user = django_user_model.objects.create(
        **{k: v for k, v in CORRECT_USER_CREATE_DATA.items() if k != 'password'}
    )
    user.set_password(CORRECT_USER_CREATE_DATA['password'])
    user.save()
    return user


@pytest.fixture
def user_db_second(django_user_model):
    user = django_user_model.objects.create(
        **{k: v for k, v in CORRECT_SECOND_USER_CREATE_DATA.items() if k != 'password'}
    )
    user.set_password(CORRECT_SECOND_USER_CREATE_DATA['password'])
    user.save()
    return user


@pytest.fixture
def auth_user_client(user_db):
    auth_client = APIClient()
    auth_client.force_authenticate(user_db)
    return auth_client


@pytest.fixture
def auth_user_second_client(user_db_second):
    auth_client = APIClient()
    auth_client.force_authenticate(user_db_second)
    return auth_client


@pytest.fixture
def anonymous_client():
    return APIClient()


@pytest.fixture
def user_register_path():
    return '/api/v1/users/'


@pytest.fixture
def user_update_retrive_path(user_db):
    return f'/api/v1/users/{user_db.pk}/'


@pytest.fixture
def token_obtain_path():
    return '/api/v1/token/'


@pytest.fixture
def token_refresh_path():
    return '/api/v1/token/refresh/'
