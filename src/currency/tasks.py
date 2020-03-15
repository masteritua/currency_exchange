
from decimal import Decimal, ROUND_HALF_DOWN
from bs4 import BeautifulSoup
from celery import shared_task
from common.functions import email
from currency import model_choices as mch
from currency.models import Rate


def save_db_date(currency, buy, sell, bank, date=None):
  buy_dec = Decimal(buy)
  buy = buy_dec.quantize(Decimal("1.00"), ROUND_HALF_DOWN)

  sell_dec = Decimal(sell)
  sell = sell_dec.quantize(Decimal("1.00"), ROUND_HALF_DOWN)

  rate_kwargs = {
    'currency': currency,
    'buy': buy,
    'sale': sell,
    'source': bank,
    'created': date,
  }

  new_rate = Rate(**rate_kwargs)
  new_rate.save()



def save_db(currency, buy, sell, bank):
    buy_dec = Decimal(buy)
    buy = buy_dec.quantize(Decimal("1.00"), ROUND_HALF_DOWN)

    sell_dec = Decimal(sell)
    sell = sell_dec.quantize(Decimal("1.00"), ROUND_HALF_DOWN)

    rate_kwargs = {
        'currency': currency,
        'buy': buy,
        'sale': sell,
        'source': bank,
    }

    # Rate.objects.create(**rate_kwargs)
    new_rate = Rate(**rate_kwargs)
    last_rate = Rate.objects.filter(currency=currency, source=bank).last()

    # from pdb import set_trace
    # set_trace()

    # if last_rate and (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
    if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
        new_rate.save()


def _alfa():
    url = 'https://alfabank.ua/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content)
    film_list = soup.find('div', {'class': 'currency-tab-block'})
    items = film_list.find_all('div', {'class': 'currency-block'})

    buy = []
    sell = []

    for item in items:
        rate = item.findAll('div', {'class': 'rate'})
        buy_block = rate[0]
        rate_number_buy = buy_block.find('span', {'class': 'rate-number'})
        buy.append(rate_number_buy.text)

        sell_block = rate[1]
        rate_number_sell = sell_block.find('span', {'class': 'rate-number'})
        sell.append(rate_number_sell.text)

    save_db(currency, buy[0], buy[1], mch.SR_ALFA)
    save_db(currency, sell[0], sell[1], mch.SR_ALFA)


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

            save_db(currency, rate['buy'], rate['sale'], mch.SR_PRIVAT)


def _aval():
    url = 'https://ex.aval.ua/ru/personal/everyday/exchange/'
    page = requests.get(url)

    soup = BeautifulSoup(page.content)
    film_list = soup.find('table', {'class': 'body-currency'})
    items = film_list.find_all('tr')
    for item in items:

        td = item.findAll('td')
        if td:
            currency_text = td[0].text

            currency = 'EUR'
            if (currency_text == "Доллары США"):
                currency = 'USD'

            buy = td[1].text
            sell = td[2].text

            save_db(currency, buy, sell, mch.SR_AVAL)


def _oshadbank():
    url = 'https://www.oschadbank.ua/ua/private/currency'
    page = requests.get(url)

    soup = BeautifulSoup(page.content)
    film_list = soup.find('table', {'class': 'table'})
    items = film_list.find_all('tr')
    for item in items:

        td = item.findAll('td')
        if td:
            currency = td[0].text
            buy = td[5].text
            sell = td[6].text

            save_db(currency, buy, sell, mch.SR_OSHADBANK)


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

            save_db(currency, Decimal(rate['rateBuy']), Decimal(rate['rateSell']), mch.SR_MONO)


@shared_task()
def parse_rates():
    _privat()
    _mono()
    _oshadbank()
    _alfa()
    _aval()


@shared_task()
def feedback_task(post):
    email(post.get('title'), post.get('text'), [post.get('email')])
