# Generated by Django 5.0.4 on 2024-09-14 19:04

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("collective_donations", "0017_alter_collect_collected_amount_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="collect",
            name="end_datetime",
            field=models.DateField(
                validators=[
                    django.core.validators.MinValueValidator(
                        limit_value=datetime.date(2024, 9, 14)
                    )
                ],
                verbose_name="Дата окончания сбора",
            ),
        ),
    ]
