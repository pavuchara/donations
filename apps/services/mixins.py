from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.permissions import BasePermission


DonationsUser = get_user_model()


class OnlyAuthorMixin(UserPassesTestMixin):
    """Миксин: Доступы только для автора объекта."""

    def test_func(self):
        object = self.get_object()
        return self.request.user == object.author


class OnlyAuthorMixinApi(BasePermission):
    """Миксин: Доступы на редактирование для автора объекта."""

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class GetUserMixin:
    """Миксин: Получение юзера."""

    def get_object(self):
        user = get_object_or_404(
            DonationsUser,
            username=self.kwargs.get('username'),
        )
        return user
