from datetime import datetime, timedelta

import requests
from currency import tasks
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Просто введите команду'

    def handle(self, *args, **options):

        for day in range(365 * 4):
            date = datetime.now() + timedelta(days=-day)
            date_format = f'{date.day}.{date.month}.{date.year}'
            link = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date_format}'
            resource = requests.get(link).json()

            for er in [8, 23]:
                data_er = resource['exchangeRate'][er]
                tasks.save_db_date(data_er['currency'], data_er['saleRateNB'], data_er['saleRate'], resource['bank'],
                                   date)
