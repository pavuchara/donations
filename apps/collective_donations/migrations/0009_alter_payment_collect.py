# Generated by Django 5.0.4 on 2024-04-27 11:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collective_donations', '0008_alter_payment_options_alter_collect_end_datetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='collect',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payments', to='collective_donations.collect', verbose_name='Сбор'),
        ),
    ]
