import asyncio

import bcrypt
from pyrogram import Client

from web.apps.bitrix24.models import Deal
from web.services.bitrix24 import bitrix24_api_service

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from web.services.telegram import telegram_service
from web.login_bot import user_bot

@csrf_exempt
def bitrix_webhook(request):
    if request.method != 'POST':
        return HttpResponse('Метод не поддерживается.', status=405)

    salt = bcrypt.gensalt()
    hashed_bitrix_app_token = bcrypt.hashpw(
        settings.BITRIX24_WEBHOOK_APPLICATION_TOKEN.encode('utf-8'),
        salt
    )
    if not bcrypt.checkpw(
        password=request.POST['auth[application_token]'].encode('utf-8'),
        hashed_password=hashed_bitrix_app_token
    ):
        return HttpResponseForbidden('Неверный application token')

    deal_id = request.POST['data[FIELDS][ID]']
    deal_data = bitrix24_api_service.crm_get_deal(deal_id=deal_id)

    if deal_data['STAGE_ID'] != 'DETAILS':
        return HttpResponse(
            'Обрабатываются сделки только '
            'со стадией "Первое КП отправлено"',
            status=400
        )

    if Deal.objects.filter(id=deal_id).exists():
        return HttpResponse(
            'Сделка уже обработана',
            status=400
        )


    telegram_username = deal_data.get(settings.BITRIX24_TELEGRAM_USERNAME_FIELD_NAME)
    if not telegram_username:
        response_text = f'По сделке <b>№{deal_id}</b> не найдено контактной информации.'
        telegram_service.send_message(
            chat_id=settings.MANAGERS_GROUP_ID,
            text=response_text
        )
        return HttpResponse(response_text, status=400)

    Deal.objects.create(
        id=deal_id,
        title=deal_data.get('TITLE'),
        telegram_username=telegram_username
    )

    user_bot.start()
    user_bot.send_message(
        chat_id=telegram_username,
        text='👋 Здравствуйте! Вчера мы отправили вам коммерческое предложение. '
             'Нам очень важно узнать ваше мнение!\n\n'
             '📊 Оцените его по шкале от 0 до 5, где\n'
             '0 - Совсем не понравилось\n'
             '5 - Всё отлично\n\n'
             'Просто отправьте цифру или оставьте отзыв в ответ на это сообщение.',
    )
    user_bot.stop()

    return HttpResponse(status=200)