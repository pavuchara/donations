from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import get_user_model


DonationsUser = get_user_model()


class OnlyAuthorMixin(UserPassesTestMixin):
    """Миксин: Доступы только для автора объекта."""

    def test_func(self):
        object = self.get_object()
        return self.request.user == object.author
