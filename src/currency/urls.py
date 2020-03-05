from django.urls import path
from currency.views import test

urlpatterns = [
    path('test', test, name='currency_test'),
]
