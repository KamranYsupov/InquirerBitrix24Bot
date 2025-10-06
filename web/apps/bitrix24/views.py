from datetime import timedelta

import bcrypt
from pyrogram import Client

from web.apps.bitrix24.models import Deal
from web.services.bitrix24 import bitrix24_api_service
import loguru
from celery.result import AsyncResult

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from web.apps.bitrix24.tasks import (
    send_message_task,
    request_deal_review_task,
    send_deal_info_to_managers_group,
)
from web.apps.bitrix24.models import Deal, ScheduledTask
from web.apps.bitrix24.utils import (
    get_tomorrow_noon,
)
from web.services.bitrix24 import bitrix24_api_service

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

    if deal_data['STAGE_ID'] != settings.MAIN_DEALS_STAGE_ID:
        return HttpResponse(
            'Обрабатываются сделки только '
            f'со стадией "{settings.MAIN_DEALS_STAGE_ID}"',
            status=400
        )

    if Deal.objects.filter(id=deal_id).exists():
        return HttpResponse(
            'Сделка уже обработана',
            status=400
        )

    telegram_username = deal_data.get(settings.BITRIX24_TELEGRAM_USERNAME_FIELD_NAME)
    deal = Deal.objects.create(
        id=deal_id,
        title=deal_data.get('TITLE'),
        telegram_username=telegram_username
    )

    if not telegram_username:
        text = (
            f'По сделке <a href="{settings.BITRIX_CRM_DEAL_URL.format(deal.id)}">'
            f'<b>"{deal.title}" (№{deal.id})</b></a>: не найдено контактной информации.'
        )
        tomorrow_noon = get_tomorrow_noon()

        send_message_task_result: AsyncResult = send_message_task.apply_async(
            kwargs=dict(chat_id=settings.MANAGERS_GROUP_ID, text=text),
            eta=tomorrow_noon,
        )
        ScheduledTask.objects.create(
            task_id=send_message_task_result.task_id,
            name='send_message_task',
            eta=tomorrow_noon
        )

        send_deal_info_task_eta = tomorrow_noon + timedelta(hours=1)
        send_deal_info_task_result = send_deal_info_to_managers_group.apply_async(
            kwargs=dict(deal_id=deal_id, check_again_tomorrow=True),
            eta=send_deal_info_task_eta,
        )
        ScheduledTask.objects.create(
            task_id=send_deal_info_task_result.task_id,
            name='send_deal_info_to_managers_group',
            eta=send_deal_info_task_eta
        )

        return HttpResponse(text, status=400)

    last_tomorrow_task_eta = (
        ScheduledTask.objects.get_last_tomorrow_task_eta(
            name='request_deal_review_task'
        )
    )
    last_tomorrow_task_eta = None
    request_deal_review_task_eta = (
        get_tomorrow_noon() if not last_tomorrow_task_eta
        else last_tomorrow_task_eta + timedelta(
            minutes=settings.REQUEST_DEAL_REVIEW_MINUTES_INTERVAL
        )
    )

    request_deal_review_task_result = request_deal_review_task.apply_async(
        args=(deal.id, ),
        eta=request_deal_review_task_eta
    )
    ScheduledTask.objects.create(
        task_id=request_deal_review_task_result.task_id,
        name='request_deal_review_task',
        eta=request_deal_review_task_eta
    )

    return HttpResponse(status=200)