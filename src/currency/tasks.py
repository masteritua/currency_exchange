from decimal import Decimal

import requests
from celery import shared_task
from currency import model_choices as mch
from currency.models import Rate


def _privat():
	url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
	response = requests.get(url)
	r_json = response.json()
	# print(r_json)

	for rate in r_json:
		if rate['ccy'] in {'USD', 'EUR'}:  # O(1) if we use list it would be O(n) ('USD', 'EUR')
			currency = mch.CURR_USD if rate['ccy'] == 'USD' else mch.CURR_EUR
			# currency = {
			#     'USD': mch.CURR_USD,
			#     'EUR': mch.CURR_EUR,
			# }[rate['ccy']]
			rate_kwargs = {
				'currency': currency,
				'buy': Decimal(rate['buy']),
				'sale': Decimal(rate['sale']),
				'source': mch.SR_PRIVAT,
			}
			# Rate.objects.create(**rate_kwargs)
			new_rate = Rate(**rate_kwargs)
			last_rate = Rate.objects.filter(currency=currency, source=mch.SR_PRIVAT).last()

			# from pdb import set_trace
			# set_trace()

			# if last_rate and (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
			if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
				new_rate.save()

			# print(Rate.objects.filter(currency=currency, source=mch.SR_PRIVAT).query)


def _mono():
	url = 'https://api.monobank.ua/bank/currency'
	response = requests.get(url)
	r_json = response.json()

	for rate in r_json:
		if rate['currencyCodeA'] in {840, 978}:
			cur = mch.CURR_USD if rate['currencyCodeA'] == 840 else mch.CURR_EUR

			currency = {
				mch.CURR_USD: 'USD',
				mch.CURR_EUR: 'EUR',
			}

			currency = currency[cur]

			rate_kwargs = {
				'currency': currency,
				'buy': Decimal(rate['rateBuy']),
				'sale': Decimal(rate['rateSell']),
				'source': mch.SR_MONO,
			}

			# Rate.objects.create(**rate_kwargs)
			new_rate = Rate(**rate_kwargs)
			last_rate = Rate.objects.filter(currency=currency, source=mch.SR_PRIVAT).last()

			# from pdb import set_trace
			# set_trace()

			# if last_rate and (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
			if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
				new_rate.save()


@shared_task()
def parse_rates():
	_privat()
	_mono()
