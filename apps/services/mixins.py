from django.contrib.auth.mixins import UserPassesTestMixin

from rest_framework.permissions import BasePermission


class OnlyAuthorMixin(UserPassesTestMixin):
    """Миксин: Доступы только для автора объекта."""

    def test_func(self):
        object = self.get_object()
        return self.request.user == object.author


class OnlyAuthorMixinApi(BasePermission):
    """Миксин: Доступы на редактирование для автора объекта."""

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
