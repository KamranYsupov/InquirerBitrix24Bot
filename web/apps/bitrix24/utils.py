from datetime import timedelta

from django.utils import timezone


def get_tomorrow_noon():
    """
    Возвращает следующий полдень (12:00)
    """
    local_tz = timezone.get_current_timezone()
    now_utc = timezone.now()
    now_local = now_utc.astimezone(local_tz)
    noon_local = now_local.replace(hour=12, minute=0, second=0, microsecond=0)

    if now_local >= noon_local:
        noon_local += timedelta(days=1)

    return noon_local.astimezone(timezone.utc)


