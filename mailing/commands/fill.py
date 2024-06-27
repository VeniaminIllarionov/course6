from django.core.management import BaseCommand
from mailing.models import Mailing, Massage, Customers, Mailing_attempt
import json


class Command(BaseCommand):

    @staticmethod
    def json_read_mailing():
        with open('mailing.json', encoding='utf-8') as json_file:
            return json.load(json_file)

    @staticmethod
    def json_read_massage():
        with open('massage.json', encoding='utf-8') as json_file:
            return json.load(json_file)

    @staticmethod
    def json_read_customers():
        with open('customers.json', encoding='utf-8') as json_file:
            return json.load(json_file)

    @staticmethod
    def json_read_mailing_attempt():
        with open('mailing_attempt', encoding='utf-8') as json_file:
            return json.load(json_file)

    def handle(self, *args, **options):

        # Удалите все рассылки
        Mailing.objects.all().delete()
        # Сброс индефикатора Рассылок
        Mailing.truncate_table_restart_id()
        # Удалите все Сообщения
        Massage.objects.all().delete()
        # Удалите все Клентов
        Customers.objects.all().delete()
        # Удалите все Настройки рассылок
        Mailing_attempt.objects.all().delete()

        mailing_list = []
        massage_list = []
        customer_list = []
        mailing_at_list = []

        # Обходим все значения категорий из фиктсуры для получения информации об одном объекте
        for mailing in Command.json_read_mailing():
            mailing_list.append(
                {"id": mailing['pk'], "send_mailing_at": mailing['fields']['send_mailing_at'],
                 "frequency": mailing['fields']['frequency'], "mailing_status": mailing['fields']['mailing_status']}
            )
        mailing_for_create = []
        for mailing_item in mailing_list:
            mailing_for_create.append(
                Mailing.objects.create(**mailing_item)
            )

        # Обходим все значения продуктов из фиктсуры для получения информации об одном объекте
        for massage in Command.json_read_massage():
            massage_list.append(
                {"id": massage['pk'], "mailing": Mailing.objects.get(pk=massage['fields']['mailing']),
                 "subject_massage": massage['fields']['subject_massage'],
                 "massage": massage['fields']['massage']}
            )
        massage_for_create = []
        for massage_item in massage_list:
            massage_for_create.append(
                Massage.objects.create(**massage_item)
            )

        # Обходим все значения продуктов из фиктсуры для получения информации об одном объекте
        for customer in Command.json_read_customers():
            customer_list.append(
                {"id": customer['pk'], "mailing": Mailing.objects.get(pk=massage['fields']['mailing']),
                 "email": customer['fields']['email'],
                 "fio": customer['fields']['fio'], "comment": customer['fields']['comment']}
            )
        customer_for_create = []
        for customer_item in customer_list:
            customer_for_create.append(
                Massage.objects.create(**customer_item)
            )

        # Обходим все значения продуктов из фиктсуры для получения информации об одном объекте
        for mailing_attempt in Command.json_read_mailing_attempt():
            mailing_at_list.append(
                {"id": mailing_attempt['pk'], "mailing": Mailing.objects.get(pk=massage['fields']['mailing']),
                 "last_attempt": mailing_attempt['fields']['last_attempt'],
                 "status": mailing_attempt['fields']['status'],
                 "mail_response": mailing_attempt['fields']['mail_response']}
            )
        mailing_attempt_for_create = []
        for mailing_attempt_item in mailing_at_list:
            mailing_attempt_for_create.append(
                Massage.objects.create(**mailing_attempt_item)
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Mailing.objects.bulk_create(mailing_for_create)
        Massage.objects.bulk_create(massage_for_create)
        Customers.objects.bulk_create(massage_for_create)
        Mailing_attempt.objects.bulk_create(massage_for_create)
