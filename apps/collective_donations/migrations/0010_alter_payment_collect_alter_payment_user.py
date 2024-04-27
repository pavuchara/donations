# Generated by Django 5.0.4 on 2024-04-27 14:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collective_donations', '0009_alter_payment_collect'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='collect',
            field=models.ForeignKey(default='Удален или не указан', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='payments', to='collective_donations.collect', verbose_name='Сбор'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(default='Удален или не указан', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='payments', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
