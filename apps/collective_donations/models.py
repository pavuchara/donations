from django.db import IntegrityError
from django.db import models, transaction
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MinValueValidator

import uuid

from apps.services import constants
from apps.services.utils import unique_slugify, message_for_author

# Получение модели пользователя.
DonationsUser = get_user_model()


class CollectPublishedManager(models.Manager):
    """
    Модельный менеджер опубликованных карточек группового денежного сбора.
    """

    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class CollectPublishedRealtedManager(CollectPublishedManager):
    """
    Модельный менеджер опубликованных карточек группового денежного сбора.
    Связанное поле - автор.
    """
    def get_queryset(self):
        return super().get_queryset().select_related('author')


class Collect(models.Model):
    """Модель: Карточка группового денежного сбора."""

    STATUS_OPTIONS = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик')
    )
    author = models.ForeignKey(
        DonationsUser,
        on_delete=models.CASCADE,
        related_name='collects',
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=constants.COLLECT_TITLE_LENGTH,
        verbose_name='Заголовок',
    )
    slug = models.SlugField(
        unique=True,
        max_length=constants.COLLECT_SLUG_MAX_LEN,
        verbose_name='URL',
    )
    occasion = models.CharField(
        max_length=constants.COLLECT_OCASSION_LENGTH,
        verbose_name='Повод',
    )
    description = models.TextField(
        max_length=constants.COLLECT_DESC_LENGTH,
        verbose_name='Описание'
    )
    target_amount = models.DecimalField(
        max_digits=constants.PAIMENT_MAX_DIGITS,
        decimal_places=constants.PAIMENT_DECIMAL_PLACES,
        verbose_name='План сбора',
        help_text=constants.MAX_PAYMENT_VALUE,
    )
    collected_amount = models.DecimalField(
        max_digits=constants.PAIMENT_MAX_DIGITS,
        decimal_places=constants.PAIMENT_DECIMAL_PLACES,
        default=0,
        verbose_name='Собрано',
    )
    contributors_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Кол-во пожертвовавших',
    )
    cover_image = models.ImageField(
        upload_to='images/collect_covers',
        default='images/default_collect.png',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=(
            'png', 'jpg', 'webp', 'jpeg', 'gif'
        ))],
        verbose_name='Изображение',
    )
    end_datetime = models.DateField(
        verbose_name='Дата окончания сбора',
        validators=[MinValueValidator(limit_value=timezone.now().date())]
    )
    create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    status = models.CharField(
        max_length=constants.COLLECT_CHOICES_LEN,
        choices=STATUS_OPTIONS,
        default='published',
        verbose_name='Статус',
    )

    objects = models.Manager()
    published = CollectPublishedManager()
    published_related = CollectPublishedRealtedManager()

    class Meta:
        ordering = ['-create']
        indexes = [
            models.Index(fields=['slug']),
        ]
        verbose_name = 'Сбор'
        verbose_name_plural = 'Сборы'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('collective_donations:collect_detail',
                       kwargs={'collect_slug': self.slug})

    def save(self, *args, **kwargs):
        """
        Генерация slug при сохранении.
        Если сбор новый, то сгенерируется на основе title
        или уникальный(если на основе title уже есть).
        Автору отправляется письмо о содании/редактировании.
        """
        subject = f'{self.title}'
        message = f'Cбор отредактирован: {self.title}'
        from_email = 'from@example.com'
        recipient_list = [self.author.email]
        if not self.pk:
            self.slug = unique_slugify(self, self.title)
            message = f'Cбор создан: {self.title}'
        # Отправка письма
        message_for_author(subject, message, from_email, recipient_list)
        super().save(*args, **kwargs)


class Payment(models.Model):
    """Модель: Платеж для сбора."""

    PAYMENT_OPTIONS = (
        ('card', 'Картой'),
        ('sbp', 'СБП'),
        ('mobile transfer', 'Перевод на телефон'),
    )

    collect = models.ForeignKey(
        Collect,
        on_delete=models.SET_NULL,
        null=True,
        related_name='payments',
        verbose_name='Сбор',
    )
    user = models.ForeignKey(
        DonationsUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='payments',
        verbose_name='Пользователь',
    )
    amount = models.DecimalField(
        max_digits=constants.PAIMENT_MAX_DIGITS,
        decimal_places=constants.PAIMENT_DECIMAL_PLACES,
        verbose_name='Сумма',
    )
    comment = models.CharField(
        max_length=constants.PAIMENT_COMMENT_MAX_LEN,
        verbose_name='Комментарий',
    )
    create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления',
    )
    payment_method = models.CharField(
        max_length=constants.PAIMENT_CHOICES_LEN,
        choices=PAYMENT_OPTIONS,
        default='card',
        verbose_name='Метод оплаты',
    )
    payment_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        verbose_name='Идентификатор оплаты',
    )

    class Meta:
        ordering = ['-create']
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f'{self.user.username}: {self.amount}'

    def get_absolute_url(self):
        return reverse('collective_donations:collect_detail',
                       kwargs={'collect_slug': self.collect.slug})

    @transaction.atomic
    def save(self, *args, **kwargs):
        """
        Проверка на уровне БД, что сумма не превышает, сумму сбора
        при добавлении новой оплаты.
        Если все ок, то доавбляется +1 к задонатившим и сумма доната.
        Автору отправляется письмо.
        """
        current_amount = self.amount + self.collect.collected_amount
        if current_amount > self.collect.target_amount:
            raise ValidationError(
                'Сумма платежа не может превышать целевую сумму сбора.'
            )

        self.collect.collected_amount += self.amount
        self.collect.contributors_count += 1
        self.collect.save()

        # Отправка письма
        subject = 'Message'
        message = f'Спасибо за донат для {self.collect.title}'
        from_email = 'from@example.com'
        recipient_list = [self.user.email]
        message_for_author(subject, message, from_email, recipient_list)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        При удалении объекта оплаты, из суммы сбора вычитается сумма оплаты.
        """
        try:
            with transaction.atomic():
                self.collect.collected_amount -= self.amount
                self.collect.contributors_count -= 1
                self.collect.save()
                super().delete(*args, **kwargs)
        except IntegrityError:
            # Можно как-то обработать ошибку.
            print('При удалении платежа возникла ошибка')
            pass
        except Exception as e:
            # Если возникла прочая ошибка.
            print(f'При удалении платежа возникла ошибка: {e}')
