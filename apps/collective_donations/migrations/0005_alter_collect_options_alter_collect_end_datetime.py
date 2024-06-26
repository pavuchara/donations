# Generated by Django 5.0.4 on 2024-04-26 11:35

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collective_donations', '0004_alter_collect_end_datetime'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collect',
            options={'ordering': ['-create'], 'verbose_name': 'Сбор', 'verbose_name_plural': 'Сборы'},
        ),
        migrations.AlterField(
            model_name='collect',
            name='end_datetime',
            field=models.DateField(validators=[django.core.validators.MinValueValidator(limit_value=datetime.date(2024, 4, 26))], verbose_name='Дата окончания сбора'),
        ),
    ]
