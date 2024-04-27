from django.core.mail import send_mail

from uuid import uuid4
from pytils.translit import slugify


def unique_slugify(instance, slug: str):
    """
    Генератор уникальных SLUG.
    Если такого slug еще нет, остается исходный.
    Если есть берется 4 рандомных знака из uuid4.
    """
    model = instance.__class__
    unique_slug = slugify(slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{unique_slug}-{uuid4().hex[:4]}'
    return unique_slug


def message_for_author(subject, message, from_email, recipient_list):
    """Отправка письма."""
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[recipient_list],
        fail_silently=True,
    )
