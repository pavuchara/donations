from django.core.mail import send_mail
from django.core.paginator import Page
from django.db.models import Model

from typing import List
from uuid import uuid4
from pytils.translit import slugify


def unique_slugify(instance: Model, slug: str):
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


def message_for_author(subject: str, message: str,
                       from_email: str, recipient_list: List[str]) -> None:
    """Отправка письма."""
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[recipient_list],
        fail_silently=True,
    )


def get_elided_paginator(page: Page, context: dict) -> dict:
    """Получение пагинатора с определенным диапазоном страниц."""
    context['paginator_range'] = page.paginator.get_elided_page_range(
        page.number,
        on_each_side=1,
        on_ends=2,
    )
    return context
