from datetime import datetime

import requests
from xml.etree import ElementTree as ET

from celery import shared_task

from exchange_rates.models import DailyExchangeRates


@shared_task
def get_exchange_rates():
    print("OK")

    response = requests.get('https://www.nbkr.kg/XML/daily.xml')

    if response.status_code == 200:
        root = ET.fromstring(response.content)

        date_str = root.get('Date')
        date = datetime.strptime(date_str, '%d.%m.%Y').date()

        usd_value = eur_value = rub_value = None

        for currency in root.findall('Currency'):
            iso_code = currency.get('ISOCode')
            value = currency.find('Value').text

            if iso_code == 'USD':
                usd_value = float(value.replace(',', '.'))
            elif iso_code == 'EUR':
                eur_value = float(value.replace(',', '.'))
            elif iso_code == 'RUB':
                rub_value = float(value.replace(',', '.'))

            if date == date.today():
                try:
                    exchange_rates = DailyExchangeRates.objects.get_or_create(date=date, usd_rate=usd_value,
                                                                              eur_rate=eur_value, rub_rate=rub_value)
                    exchange_rates.save()
                except Exception as e:
                    print("Ошибка при получении курсов валют.")
        else:
            print("Ошибка при выполнении запроса:", response.status_code)
