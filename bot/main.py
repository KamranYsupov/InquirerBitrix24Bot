import os
from copy import copy

import django
import loguru
from django.conf import settings
from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram import types

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.core.settings')

django.setup()

USERBOT_DATA = copy(settings.USERBOT_DATA)
USERBOT_DATA.pop('workdir')

user_bot = Client(**settings.USERBOT_DATA)

from web.services.telegram import telegram_service
from web.apps.bitrix24.models import Deal

@user_bot.on_message()
def handel_deal(client: Client, message: types.Message):
    deal = Deal.objects.filter(telegram_username=message.from_user.username)
    if not deal.exists():
        return

    deal = deal.first()

    if deal.user_review is not None:
        return

    try:
        user_review = int(message.text)
    except ValueError:
        client.send_message(
            chat_id=message.from_user.id,
            text='Пожалуйста, отправьте корректную оценку.',
        )
        return

    if user_review not in range(6):
        client.send_message(
            chat_id=message.from_user.id,
            text='Пожалуйста, отправьте оценку от 0 до 5.',
        )
        return

    deal.user_review = user_review
    deal.save()

    client.send_message(
        chat_id=message.from_user.id,
        text='Спасибо за вашу оценку!',
    )

    telegram_service.send_message(
        chat_id=settings.MANAGERS_GROUP_ID,
        text=f'Оценка по сделке <b>№{deal.id}</b>: {user_review}',
    )




if __name__ == '__main__':
    loguru.logger.info('UserBot is starting...')
    user_bot.run()


