# Generated by Django 4.2.1 on 2025-03-20 13:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bitrix_deal_id', models.PositiveIntegerField(editable=False, unique=True, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=150, null=True, verbose_name='Название')),
                ('telegram_username', models.CharField(max_length=150)),
                ('user_review', models.PositiveIntegerField(default=None, null=True, validators=[django.core.validators.MaxValueValidator(5)], verbose_name='Оценка пользователя')),
            ],
        ),
    ]
