import pytest
from django.urls import reverse
from currency.tasks import _privat, _mono
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



class Response:
    pass




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
    assert response.json()['id'] == 1


def test_rate_json_id_status(api_client):

    url = reverse('api-currency:rates')
    response = api_client.post(url, {"currency": 1, "buy": 11, "sale": 5, "source": 1}, format='json')
    assert response.status_code == 201

def test_getlist(api_client):

    url = reverse('api-currency:contacts')
    response = api_client.get(url, {}, format='json')
    assert response.json() == []


def test_create(api_client):
    url = reverse('api-currency:contacts')
    response = api_client.post(url, {
        "email": "masteritua@gmail.com",
        "title": "Test POST",
        "body": "Test POST"
    }, format='json')
    assert response.json()['id'] == 1


def test_get_obj_by_id(api_client):
    url = "/api/v1/currency/contact/1"
    response = api_client.get(url, {}, format='json')
    assert response.json()['id'] == 1

def test_update_one(api_client):
    url = "/api/v1/currency/contact/1"
    response = api_client.patch(url, {"email": "test@test.com"}, format='json')
    assert 'test@test.com' == response.json()['email']


def test_delete_obj(api_client):
    url = "/api/v1/currency/contact/1"
    api_client.delete(url)
    response=api_client.get(url)
    assert response.json()['detail'] == 'Not found.'


def test_privat(mocker):

    def mock():
        response = Response()
        response.json = lambda: [{
                            "ccy": "USD",
                            "base_ccy": "UAH",
                            "buy": "27.10000",
                            "sale": "27.65000",
                        },
                        {
                            "ccy": "EUR",
                            "base_ccy": "UAH",
                            "buy": "29.20000",
                            "sale": "29.86000",
                        }]
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()

    _privat()


def test_monobank(mocker):

    def mock():
        response = Response()
        response.json = lambda: [{
            "currencyCodeA": "840",
            "currencyCodeB": "980",
            "date":	"1585948209",
            "rateBuy": "27.35",
            "rateSell": "27.6197",
        },
        {
            "currencyCodeA": "978",
            "currencyCodeB": "840",
            "date": "1585948209",
            "rateBuy": "1.0863",
            "rateSell": "1.1094",
        }]
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()

    _mono()