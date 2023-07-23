from http import HTTPStatus

import requests
from django.test import TestCase

from app.utils import get_currency_rate


class CurrencyTestCase(TestCase):

    def test_api_http_status_code(self):
        url = 'https://api.vatcomply.com/rates?base=USD&date=10/01/2000'
        response = requests.get(url)

        self.assertTrue(response.status_code,HTTPStatus.OK)

    def test_get_currency_date_return_dates_list(self,):
        currencies_list = get_currency_rate('10/01/2000','15/01/2000')

        self.assertIsInstance(currencies_list,list)