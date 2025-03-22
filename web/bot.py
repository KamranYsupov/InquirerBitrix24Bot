import asyncio
import os

import django
import loguru
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram import types

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.core.settings')

django.setup()

from pyrogram import Client

user_bot = Client(
    name=settings.USERBOT_LOGIN,
    api_id=settings.TELEGRAM_API_ID,
    api_hash=settings.TELEGRAM_API_HASH,
    phone_number=settings.USERBOT_PHONE,
    parse_mode=ParseMode.HTML,
    workdir=str(settings.BASE_DIR),
)


if __name__ == '__main__':
    loguru.logger.info('UserBot is starting...')
    user_bot.run()
