from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


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

    telegram_username = models.CharField(max_length=150)
    user_review = models.PositiveIntegerField(
        'Оценка пользователя',
        validators=[
            MaxValueValidator(5),
        ],
        null=True,
        default=None
    )
