from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from user_app import constants


class DonationsUser(AbstractUser):
    """Кастомная модель прользователя."""

    paternal_name = models.CharField(
        max_length=constants.PATERNAL_NAME_LEN,
        blank=True,
        null=True,
        verbose_name='Отчество',
    )
    email = models.EmailField(
        unique=True,
        blank=False,
        verbose_name='Электронная почта',
    )
    avatar = models.ImageField(
        upload_to='images/user_avatar',
        default='images/default_user.jpg',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=(
            'png', 'jpg', 'jpeg'
        ))],
        verbose_name='Аватар',
    )
    bio = models.TextField(
        max_length=constants.BIO_MAX_LENGTH,
        blank=True,
        verbose_name='О себе',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def clean(self):
        super().clean()
        if not self.email:
            raise ValidationError(
                'Email обязательное поле, пожалуйста, заполните'
            )

    def get_absolute_url(self):
        return reverse('user_app:profile_detail',
                       kwargs={'username': self.username})

    def get_full_name(self):
        return f'{self.first_name} {self.last_name} {self.paternal_name}'
