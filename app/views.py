from datetime import datetime

from django.contrib import messages
from django.shortcuts import render
from django.views import View

from app.models import CurrencyRate
from app.utils import get_currency_rate

from .models import CurrencyRate


class HomeView(View):
    def get(self, request):
        """
        Método GET da view HomeView.
        
        Este método é responsável por exibir a página inicial ('index.html') com as últimas consultas salvas no banco de dados.

        Args:
            request (HttpRequest): Objeto HttpRequest contendo os dados da requisição HTTP.

        Returns:
            HttpResponse: Retorna a renderização da página 'index.html' com os dados das últimas consultas ('consults') no contexto.
        """
        
        # Consultar as últimas 3 consultas salvas no banco de dados, ordenando por data de criação decrescente
        consults = CurrencyRate.objects.all().order_by('-created_at')[:3]

        # Criar o contexto com as consultas e renderizar a página 'index.html'
        context = {'consults': consults}

        return render(request, 'home/index.html', context)
    
    def post(self, request):
        """
        Método POST da view HomeView.
        
        Este método é responsável por processar os dados enviados por meio do formulário na página 'index.html'.

        Args:
            request (HttpRequest): Objeto HttpRequest contendo os dados da requisição HTTP.

        Returns:
            HttpResponse: Retorna a renderização da página 'index.html' caso ocorra um erro na consulta, ou a renderização da página 'chart.html' com os dados da consulta no contexto.
        """
       
        if request.method == 'POST':
            # Obter os dados do formulário
            date1 = request.POST['start_date']
            date2 = request.POST['end_date']
            currency = request.POST['inlineRadioOptions']

            # Obter as cotações com base nas datas e moeda selecionadas
            quotes_list = get_currency_rate(date1, date2)
            
            if 'A diferença entre as datas deve ser menor' in quotes_list:
                # Exibir uma mensagem de erro caso ocorra um problema na consulta
                messages.warning(request, quotes_list)
                return render(request, 'home/index.html')
            
            #Certificando que a data final nao pode ser anterior a data inicial
            if datetime.strptime(date1, '%d/%m/%Y') > datetime.strptime(date2, '%d/%m/%Y'):
                messages.warning(request, 'A data inicial escolhida é menor que a data final')
                return render(request, 'home/index.html')

            else:
                dates = []
                rates = []

                # Processar as cotações para formatar as datas e obter as taxas na moeda selecionada
                for item in quotes_list:
                    data_obj = datetime.strptime(item['date'], "%Y-%m-%d")
                    data_formatada = data_obj.strftime("%d/%m/%Y")
                    dates.append(data_formatada)

                    rate = round(item['rates'][currency], 4)
                    rates.append(rate)

                # Armazenar os dados da consulta no banco de dados
                currency_rate = CurrencyRate(
                    coin=f'USD x {currency} [{date1} - {date2}]',
                    dates=dates,
                    rates=rates,
                )
                currency_rate.save()

                # Criar o contexto com os dados da consulta e renderizar a página 'chart.html'
                context = {'dates': dates, 'rates': rates, 'text': f'Valores de USD x {currency}'}
                return render(request, 'home/chart.html', context)


class ChartView(View):
    def get(self, request):
        # Recuperar os parâmetros da URL
        coin = request.GET.get('coin')
        dates = request.GET.get('dates')
        rates = request.GET.get('rates')

        # Passa os dados para o template 'chart.html'
        context = {
            'text': coin,
            'dates': dates,
            'rates': rates,
        }
        return render(request, 'home/chart.html', context)
