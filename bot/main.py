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

user_bot = Client(**USERBOT_DATA)

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

    if len(message.text) > 200:
        message.reply('Максимальная длина отзыва: 200 символов')
        return

    deal.user_review = message.text
    deal.save()

    message.reply('Спасибо за вашу оценку!')

    telegram_service.send_message(
        chat_id=settings.MANAGERS_GROUP_ID,
        text=(
            f'Отзыв по сделке '
            f'<a href="{settings.BITRIX_CRM_DEAL_URL.format(deal.id)}">'
            f'<b>"{deal.title}" (№{deal.id})</b></a>: {deal.user_review}'
        ),
    )


if __name__ == '__main__':
    loguru.logger.info('UserBot is starting...')
    user_bot.run()


