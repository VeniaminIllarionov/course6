from logging import Logger

from django.core.cache import cache
from config.settings import CACHE_ENABLED
import pytz
from datetime import timedelta, datetime

from config import settings
from django.core.mail import send_mail

from mailing.models import Mailing, Massage, Customers, Mailing_attempt


def get_qs_from_cache(qs, key):
    if not CACHE_ENABLED:
        return qs
    objects = cache.get(key)
    if objects is not None:
        return objects
    objects = qs
    cache.set(key, qs)
    return objects


def my_job():
    day = timedelta(days=1)
    week = timedelta(days=7)
    month = timedelta(days=31)

    zone = pytz.timezone(settings.TIME_ZONE)
    today = datetime.now(zone)
    mailings = Mailing.objects.all().filter(is_active=True)

    for mailing in mailings:
        if mailing.status != 'finished':
            mailing.status = 'executing'
            mailing.save()
            emails_list = [client.email for client in mailing.client.all()]

            print(f'Рассылка {mailing.id} - начало {mailing.start_time}; конец {mailing.end_time}')

            result = send_mail(
                subject=Massage.subject_massage,
                message=Massage.massage,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=emails_list
            )
            print('Пошла рассылка')

            status = result == True

            log = Mailing_attempt(mailing=mailing, status=status)
            log.save()

            if mailing.frequency == 'per_day':
                mailing.next_date = log.last_time_sending + day
            elif mailing.frequency == 'per_week':
                mailing.next_date = log.last_time_sending + week
            elif mailing.frequency == 'per_month':
                mailing.next_date = log.last_time_sending + month

            if status:  # на случай сбоя рассылки она останется активной
                if mailing.next_date < mailing.end_time:
                    mailing.status = 'created'
                else:
                    mailing.status = 'finished'

            mailing.save()
            print(f'Рассылка {mailing.mailing_name} отправлена {today} (должна была {mailing.next_date})')
