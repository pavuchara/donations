# Generated by Django 5.0.4 on 2024-04-27 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0004_donationsuser_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationsuser',
            name='paternal_name',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Отчество'),
        ),
    ]