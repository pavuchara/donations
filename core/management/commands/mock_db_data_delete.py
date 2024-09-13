"""
Удаление всех данных из БД кроме суперюзера.
Вызов командой: python manage.py mock_db_data_delete
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from collective_donations.models import Collect, Payment

# Получение модели пользователя.
DonationsUser = get_user_model()


class Command(BaseCommand):
    help = 'Удаление всех моковых данных, кроме суперюзера'

    def handle(self, *args, **options):
        # Удаление всех оплат.
        Payment.objects.all().delete()

        # Удаление всех карточек сбора.
        Collect.objects.all().delete()

        # Получение всех пользователей кроме суперюзера.
        superusers = DonationsUser.objects.filter(is_superuser=True)

        # Удаление всех пользователей кроме суперюзера.
        DonationsUser.objects.exclude(pk__in=superusers).delete()

        self.stdout.write(self.style.SUCCESS(
            'Все данные, кроме суперпользователя, успешно удалены.'
            ))
