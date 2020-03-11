from django.core.mail import send_mail
from django.conf import settings
from smtplib import SMTPException
from django.core.files import File


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