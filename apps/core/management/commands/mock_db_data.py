"""
Создание моковых данных.
Вызов командой: python manage.py mock_db_data
"""


from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model

import random

from apps.collective_donations.models import Collect, Payment


# Получение модель пользователя.
DonationsUser = get_user_model()

# Создаваемое кол-во пользователей.
USERS_COUNT = 50

# Создаваемое кол-во карточек сбора.
COLLECTS_COUNT = 100

# Создаваемое кол-во донатов для кажой карточки (ОТ 0 ДО PAYMENT_COUNT).
# !!!ЭТО ВЕРХНЯЯ ГРАНИЦА РАНДОМА!!!
# необходимо установить <= 10 или изменить суммы доната для корректной работы.
PAYMENT_COUNT = 10


class Command(BaseCommand):
    help = ('Заполнение БД моковыми данными '
            '!!!Локально создаются email на каждый сбор и донат!!!'
            'Для отключения сообщений на время доната необходимо'
            'Установить флаг в apps.services.constants.SEND_EMAILS False')

    def handle(self, *args, **options):
        # Пользователи.
        for i in range(USERS_COUNT):
            DonationsUser.objects.create(
                first_name=f'user{i}',
                last_name=f'user{i}',
                paternal_name=f'user{i}',
                username=f'user{i}',
                email=f'user{i}@example.com',
            )

        # Карточки сбора.
        for i in range(COLLECTS_COUNT):
            collect = Collect.objects.create(
                author=random.choice(DonationsUser.objects.all()),
                title=f'Collect {i}',
                slug=f'collect-{i}',
                occasion='Occasion',
                description='Description',
                target_amount=random.randint(1000, 10000),
                collected_amount=0,
                contributors_count=0,
                end_datetime=timezone.now().date(),
                status='published',
            )

            # Оплата для сбора.
            for j in range(random.randint(0, 10)):
                Payment.objects.create(
                    collect=collect,
                    user=random.choice(DonationsUser.objects.all()),
                    amount=random.randint(1, 50),
                    comment='Comment',
                    create=timezone.now(),
                    payment_method=random.choice(
                        ['card', 'sbp', 'mobile transfer']
                    ),
                )

        self.stdout.write(self.style.SUCCESS('БД успешно наполнена.'))
