from django.contrib.auth.mixins import UserPassesTestMixin


class OnlyAuthorMixin(UserPassesTestMixin):
    """Миксин: Доступы только для автора объекта."""

    def test_func(self):
        object = self.get_object()
        return self.request.user == object.author
