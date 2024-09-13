from django.core.mail import send_mail
from donations.celery import app


@app.task
def send_mail_task(subject, message, from_email, recipient_list, fail_silently):
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=fail_silently,
    )
