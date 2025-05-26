import asyncio
import os

import django
import loguru
from django.conf import settings
from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.enums import ParseMode

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.core.settings')

django.setup()

from pyrogram import Client

user_bot = Client(**settings.USERBOT_DATA)

if __name__ == '__main__':
    loguru.logger.info('UserBot is starting...')
    user_bot.run()
