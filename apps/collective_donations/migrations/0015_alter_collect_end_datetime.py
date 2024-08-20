# Generated by Django 5.0.4 on 2024-08-20 15:36

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("collective_donations", "0014_alter_collect_end_datetime"),
    ]

    operations = [
        migrations.AlterField(
            model_name="collect",
            name="end_datetime",
            field=models.DateField(
                validators=[
                    django.core.validators.MinValueValidator(
                        limit_value=datetime.date(2024, 8, 20)
                    )
                ],
                verbose_name="Дата окончания сбора",
            ),
        ),
    ]
