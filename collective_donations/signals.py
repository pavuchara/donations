from django.dispatch import receiver
from django.db.models.signals import post_save

from core import constants
from collective_donations.tasks import send_mail_task
from collective_donations.models import Payment


@receiver(post_save, sender=Payment)
def post_create_payment(sender, instance, *args, **kwargs) -> None:
    """Отправка письма."""
    if constants.SEND_EMAILS:
        domain = "http://127.0.0.1:8000"
        message_for_donator = f'Спасибо за донат!\n {domain}{instance.collect.get_absolute_url()}'
        message_for_recipient = f'Пришел донат! {instance.amount}р.\n {domain}{instance.collect.get_absolute_url()}'

        send_mail_task.delay(
            subject='Donations',
            message=message_for_donator,
            from_email='admin@localhost.ru',
            recipient_list=[instance.user.email],
            fail_silently=True,
        )

        send_mail_task.delay(
            subject='Donations',
            message=message_for_recipient,
            from_email='admin@localhost.ru',
            recipient_list=[instance.collect.author.email],
            fail_silently=True,
        )
