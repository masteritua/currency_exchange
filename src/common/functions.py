from django.core.mail import send_mail
from django.conf import settings
from smtplib import SMTPException
from django.core.files import File
from decimal import Decimal, ROUND_HALF_DOWN
from currency.models import Rate

def save_to_file(text):
    with open(settings.EMAIL_FILE_PATH_REPORT, 'w') as f:
        myfile = File(f)
        myfile.write(text)


def email(subject, message, recipient_list=None):
    email_from = settings.EMAIL_HOST_USER

    if not recipient_list:
        recipient_list = ['masteritua@gmail.com']


    try:
        send_mail(
            subject,
            message,
            email_from,
            recipient_list,
            fail_silently=False
        )

        save_to_file(subject)

    except SMTPException as e:

        save_to_file(f'Ошибка отправки письма: {e}')


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

    new_rate = Rate(**rate_kwargs)
    last_rate = Rate.objects.filter(currency=currency, source=bank).last()


    if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
        new_rate.save()