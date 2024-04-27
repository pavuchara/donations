from django import template

from apps.collective_donations.models import Collect, Payment


register = template.Library()


@register.simple_tag
def total_collects():
    """Кол-во сборов."""
    return Collect.published.count()


@register.simple_tag
def total_payments():
    """Кол-во донатов."""
    return Payment.objects.count()
