from datetime import datetime

import loguru
from django.db import models
from django.core.validators import MaxValueValidator
from django.utils import timezone

from web.apps.bitrix24.utils import get_tomorrow_noon


class Deal(models.Model):
    """Модель сделки"""
    id = models.PositiveIntegerField(
        'ID',
        editable=False,
        unique=True,
        primary_key=True,
    )
    title = models.CharField(
        'Название',
        null=True,
        default=None,
        max_length=150
    )
    is_active = models.BooleanField(
        'Активна',
        default=False
    )

    telegram_username = models.CharField(max_length=150)
    user_review = models.PositiveIntegerField(
        'Оценка пользователя',
        validators=[
            MaxValueValidator(5),
        ],
        null=True,
        default=None
    )

    def __str__(self):
        return self.title


class ScheduledTask(models.Model):
    eta = models.DateTimeField()
    name = models.CharField(
        max_length=250,
        db_index=True,
        null=True,
        default=None,
    )
    task_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class ScheduledTaskManager(models.Manager):
        def get_last_tomorrow_task_eta(self, **kwargs) -> datetime:
            last_tomorrow_task_eta = (
                self.filter(eta__gte=get_tomorrow_noon(), **kwargs)
                .order_by('-eta')
                .values_list('eta', flat=True)
            ).first()
            loguru.logger.info(last_tomorrow_task_eta)

            return last_tomorrow_task_eta

    objects = ScheduledTaskManager()




