from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from app.models import CurrencyRate
from app.views import ChartView, HomeView


class TestHomeView(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')

    def test_home_get_returns_correct_html(self,):
        response = self.client.get(self.home_url)

        self.assertEqual(response.status_code,HTTPStatus.OK)
        self.assertTemplateUsed(response,'home/index.html')

    def test_home_post_request(self,):
        form_data = {
            'start_date': '13/01/2000',
            'end_date': '10/01/2000',
            'inlineRadioOptions':'USD'
        }
        # Realizar a requisição POST para a view HomeView com os dados do formulário
        response = self.client.post(self.home_url, data=form_data)

        self.assertTrue(response, HTTPStatus.OK)


class TestChartView(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('chart_view')

    def test_home_get_returns_correct_html(self,):
        response = self.client.get(self.home_url)

        self.assertEqual(response.status_code,HTTPStatus.OK)
        self.assertTemplateUsed(response,'home/chart.html')

    def test_get_with_params(self):
            # Define os parâmetros da URL para o teste
            coin = 'USD x BRL'
            dates = '["30/06/2023", "01/07/2023"]'
            rates = '[4.8581, 4.7787]'

            # Monta a URL com os parâmetros
            url = reverse('chart_view') + f'?coin={coin}&dates={dates}&rates={rates}'

            # Realiza a requisição GET para a view com os parâmetros na URL
            response = self.client.get(url)

            # Verifica se a resposta tem o status code 200 (sucesso)
            self.assertEqual(response.status_code, 200)

            # Verifica se os parâmetros foram passados para o template
            self.assertContains(response, coin)
            self.assertContains(response, dates)
            self.assertContains(response, rates)
