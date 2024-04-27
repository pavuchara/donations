# Generated by Django 5.0.4 on 2024-04-26 17:43

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collective_donations', '0006_alter_collect_cover_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Идентификатор оплаты'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('card', 'Картой'), ('sbp', 'СБП'), ('mobile transfer', 'Перевод на телефон')], default='card', max_length=15, verbose_name='Метод оплаты'),
        ),
    ]
