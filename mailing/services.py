from logging import Logger
from time import sleep
import time
import re

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.cache import cache
from config.settings import CACHE_ENABLED
import pytz
from datetime import timedelta, datetime

from config import settings

from mailing.models import Mailing, Mailing_attempt
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

            result = send_mail(
                subject=mailing.massage.subject_massage,
                message=mailing.massage.massage,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[client.email for client in client]

            )

            if mailing.start_time is None:
                mailing.start_time = today
                mailing.save()

            if mailing.end_time is None:
                mailing.end_time = mailing.start_time
                mailing.next_day = mailing.start_time
                mailing.save()

            print('Пошла рассылка')

            print(f'Рассылка {mailing.id} - начало {mailing.start_time}; конец {mailing.end_time}')


            status = result == True

            log = Mailing_attempt(status=status)
            log.save()

            if mailing.frequency == 'per_day':
                mailing.next_day = log.last_attempt + day
            elif mailing.frequency == 'per_week':
                mailing.next_day = log.last_attempt + week
            elif mailing.frequency == 'per_month':
                mailing.next_day = log.last_attempt + month

            if status:  # на случай сбоя рассылки она останется активной
                if mailing.next_day < mailing.end_time:
                    mailing.mailing_status = 'executing'
                else:
                    mailing.mailing_status = 'finished'
                    print('Я все')

            mailing.save()
            print(f'Рассылка {mailing.id} отправлена {today} (должна была {mailing.next_day})')
            print(mailing.mailing_status)




def start_scheduler():
    scheduler = BackgroundScheduler()

    # Проверка, добавлена ли задача уже
    if not scheduler.get_jobs():
        scheduler.add_job(my_job, 'interval', seconds=10)

    if not scheduler.running:
        scheduler.start()





