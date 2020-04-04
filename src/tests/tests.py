import pytest
from django.urls import reverse
from currency.tasks import _privat
from account.models import User
from django.core import mail
from account.tasks import send_activation_code_async
from uuid import uuid4


def test_sanity():
    assert 200 == 200


def test_index_page(client):
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200


def test_rates_not_auth(client):

    url = reverse('api-currency:rates')
    response = client.get(url)
    assert response.status_code == 401
    resp_j = response.json()
    assert len(resp_j) == 1
    assert resp_j['detail'] == 'Authentication credentials were not provided.'


def test_rates_auth(api_client, user):
    url = reverse('api-currency:rates')
    response = api_client.get(url)
    assert response.status_code == 401

    api_client.login(user.username, user.raw_password)
    response = api_client.get(url)
    assert response.status_code == 200


def test_get_rates(api_client, user):
    url = reverse('api-currency:rates')
    api_client.login(user.email, user.raw_password)
    response = api_client.get(url)
    assert response.status_code == 200

    # response = api_client.post(url, data={}, format='json')

    # response = api_client.put(url + id, data={}, format='json')
    # response = api_client.delete(url + id, data={}, format='json')


class Response:
    pass


def test_task(mocker):


    def mock():
        response = Response()
        response.json = lambda: [{'ccy': 'USD'}]
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()

    _privat()

def test_send_email():

    emails = mail.outbox
    print('EMAILS:', emails)

    send_activation_code_async.delay(1, str(uuid4()))
    emails = mail.outbox
    assert len(emails) == 1

    email = mail.outbox[0]
    assert email.subject == 'Your activation code'


# test API
def test_rate_json(api_client, user):

    url = reverse('api-currency:rates')
    response = api_client.get(url, {}, format='json')
    assert response.json() == []


def test_rate_json_id(api_client):

    url = reverse('api-currency:rates')
    response = api_client.post(url, {"currency": 1, "buy": 11, "sale": 5, "source": 1}, format='json')
    assert response.json()['id']


def test_rate_json_id_status(api_client):

    url = reverse('api-currency:rates')
    response = api_client.post(url, {"currency": 1, "buy": 11, "sale": 5, "source": 1}, format='json')
    assert response.status_code == 201



'''
    Testing db
 
    1. Написать тесты на ContactUs API. 
    Покрыть след. случаи: 
    - получение списка, 
    - создание обьекта, 
    - получение одного обьекта по айди, 
    - одновление одного обьекта, 
    - удаление обьекта.
    3. Протестировать таки по парсингу курсов:
    - ПриватБанк 
    - МоноБанк.
'''


def test_contact_us(api_client):
    pass


def test_getlist(api_client):
    pass


def test_create(api_client):
    pass


def test_get_obj_by_id(api_client):
    pass

def test_update_one(api_client):
    pass


def test_delete_obj(api_client):
    pass

def test_api_privat(api_client):
    pass

def test_delete_monobank(api_client):
    pass