from logging import Logger

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.cache import cache
from config.settings import CACHE_ENABLED
import pytz
from datetime import timedelta, datetime

from config import settings

from mailing.models import Mailing, Massage, Customers, Mailing_attempt
from django.core.mail import send_mail


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
        client = mailing.clients.all()
        if mailing.mailing_status != 'finished':
            mailing.mailing_status = 'executing'
            mailing.save()
            emails_list = [client.email for client in client]

            print(f'Рассылка {mailing.id} - начало {mailing.start_time}; конец {mailing.end_time}')

            result = send_mail(
                subject=Massage.subject_massage,
                message=Massage.massage,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=emails_list

            )
            print('Пошла рассылка')

            status = result == True

            log = Mailing_attempt(status=status)
            log.save()

            if mailing.frequency == 'per_day':
                mailing.next_date = log.last_attempt + day
            elif mailing.frequency == 'per_week':
                mailing.next_date = log.last_attempt + week
            elif mailing.frequency == 'per_month':
                mailing.next_date = log.last_attempt + month

            if status:  # на случай сбоя рассылки она останется активной
                if mailing.next_date < mailing.end_time:
                    mailing.status = 'created'
                else:
                    mailing.status = 'finished'

            mailing.save()
            print(f'Рассылка {mailing.id} отправлена {today} (должна была {mailing.next_date})')


def start_scheduler():
    scheduler = BackgroundScheduler()

    # Проверка, добавлена ли задача уже
    if not scheduler.get_jobs():
        scheduler.add_job(my_job, 'interval', seconds=10)

    if not scheduler.running:
        scheduler.start()
