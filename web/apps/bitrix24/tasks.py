import asyncio
from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.utils import timezone
from pyrogram import Client

from web.apps.bitrix24.models import Deal, ScheduledTask
from web.apps.bitrix24.utils import get_tomorrow_noon
from web.services.bitrix24 import bitrix24_api_service
from web.services.telegram import telegram_service


@shared_task(ignore_result=True)
def send_message_task(
        chat_id: str | int,
        text: str,
        use_userbot: bool = False

):
    kwargs = dict(chat_id=chat_id, text=text)

    if not use_userbot:
        telegram_service.send_message(**kwargs)

        return

    async def send_userbot_message_with_context():
        async with Client(**settings.USERBOT_DATA) as client:
            await client.send_message(**kwargs)

    asyncio.run(send_userbot_message_with_context())


@shared_task(ignore_result=True)
def request_deal_review_task(
        deal_id: int,
):
    deal = Deal.objects.get(id=deal_id)
    deal.is_active = True
    deal.save()

    send_message_task(
        chat_id=deal.telegram_username,
        text=(
            '👋 Здравствуйте! Мы отправили вам коммерческое предложение. '
            'Нам очень важно узнать ваше мнение!\n\n'
            '📊 Оцените его по шкале от 0 до 5, где\n'
            '0 - Совсем не понравилось\n'
            '5 - Всё отлично\n\n'
            'Просто отправьте цифру или оставьте отзыв в ответ на это сообщение.'
        ),
        use_userbot=True
    )


@shared_task(ignore_result=True)
def send_deal_info_to_managers_group(
        deal_id: int,
        check_again_tomorrow: bool = False
):
    deal_data = bitrix24_api_service.crm_get_deal(deal_id=deal_id)
    telegram_username = deal_data.get(settings.BITRIX24_TELEGRAM_USERNAME_FIELD_NAME)
    if telegram_username:
        Deal.objects.filter(id=deal_id).update(telegram_username=telegram_username)

        last_tomorrow_task_eta = (
            ScheduledTask.objects.get_last_tomorrow_task_eta(
                name='request_deal_review_task'
            )
        )
        request_deal_review_task_eta = (
            get_tomorrow_noon() if not last_tomorrow_task_eta
            else last_tomorrow_task_eta + timedelta(
                minutes=settings.REQUEST_DEAL_REVIEW_MINUTES_INTERVAL
            )
        )

        result = request_deal_review_task.apply_async(
            args=(deal_id, ),
            eta=request_deal_review_task_eta
        )
        ScheduledTask.objects.create(
            task_id=result.task_id,
            name='request_deal_review_task',
            eta=request_deal_review_task_eta
        )
        return

    text = f'По сделке <b>№{deal_id}</b> '

    if not check_again_tomorrow:
        text += (
            'не была запрошена обратная '
            'связь из-за отсутствия контактной информации.'
        )

    else:
        text += 'не найдено контактной информации.'
        tomorrow_noon = get_tomorrow_noon()
        result = send_deal_info_to_managers_group.apply_async(
            args=(deal_id,),
            eta=tomorrow_noon
        )
        ScheduledTask.objects.create(
            task_id=result.task_id,
            name='send_deal_info_to_managers_group',
            eta=tomorrow_noon
        )

    telegram_service.send_message(
        chat_id=settings.MANAGERS_GROUP_ID,
        text=text
    )


@shared_task
def cleanup_old_tasks():
    # Удаляем задачи старше 7 дней
    ScheduledTask.objects.filter(created_at__lt=timezone.now()-timedelta(days=7)).delete()



