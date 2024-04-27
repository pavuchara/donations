# Generated by Django 5.0.4 on 2024-04-26 11:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collective_donations', '0005_alter_collect_options_alter_collect_end_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collect',
            name='cover_image',
            field=models.ImageField(blank=True, default='images/default_collect.png', null=True, upload_to='images/collect_covers', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))], verbose_name='Изображение'),
        ),
    ]
