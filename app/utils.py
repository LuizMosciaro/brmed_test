import os
from datetime import datetime, timedelta

import numpy as np
import requests

def get_currency_rate(start_date, end_date):
    """
    Obtém as taxas de câmbio do USD (Dólar Americano) em relação à moeda base para um período de tempo especificado.

    Args:
        start_date (str): Data de início do período no formato 'dd/mm/aaaa'.
        end_date (str): Data de término do período no formato 'dd/mm/aaaa'.

    Returns:
        list: Uma lista contendo os dados de taxas de câmbio para cada dia útil no período especificado.
              Cada item da lista é um dicionário contendo as taxas de câmbio para a moeda base (USD) em relação a outras moedas
              para o dia específico. Exemplo de formato:
              [
                  {
                      "date": "2023-06-30",
                      "base": "USD",
                      "rates": {
                          "BRL": 4.8581,
                          "EUR": 0.8785,
                          ...
                      }
                  },
                  ...
              ]

        str: Uma mensagem de erro informando que a diferença entre as datas deve ser menor ou igual a 5 dias úteis, 
             se o período especificado exceder o limite de 5 dias úteis.

    Raises:
        Exception: Caso ocorra algum erro durante a obtenção das taxas de câmbio.

    Note:
        Este método usa a API de taxas de câmbio da VATComply (https://www.vatcomply.com/) para obter as taxas de câmbio.
        É necessário ter um cadastro e gerar chaves de API válidas para usar a API. As chaves de API são armazenadas
        como variáveis de ambiente no sistema operacional, o que garante a segurança e confidencialidade das informações.

    """
    try:
        # Converter strings de data para objetos datetime
        start_date = datetime.strptime(start_date, '%d/%m/%Y')
        end_date = datetime.strptime(end_date, '%d/%m/%Y')

        # Converter as datas em numpy.datetime64 com unidade diária (D)
        start_date_np = np.datetime64(start_date, 'D')
        end_date_np = np.datetime64(end_date, 'D')

        # Contar o número de dias úteis entre as datas
        business_days = np.busday_count(start_date_np, end_date_np)

        if business_days > 5:
            return 'A diferença entre as datas deve ser menor ou igual a 5 dias úteis.'

        else:
            # Criar uma lista de datas úteis usando numpy
            dates_list = np.arange(start_date_np, end_date_np, dtype="datetime64[D]")

            currencies_list = []
            for date in dates_list:
                # Configurar o proxy com as credenciais de autenticação
                proxy = {
                    "http": "http://{}:{}@{}".format(
                        os.getenv('USERNAME'), os.getenv('PASSWORD'), os.getenv('GEONODE_DNS')
                    )
                }
                # Converter a data de numpy.datetime64 para string no formato 'aaaa-mm-dd'
                date_str = np.datetime_as_string(date, unit='D')

                # Montar a URL para fazer a requisição das taxas de câmbio
                url = f'https://api.vatcomply.com/rates?base=USD&date={date_str}'
                response = requests.get(url, proxies=proxy)

                if response.status_code == 200:
                    # Se a requisição for bem-sucedida, adicionar os dados na lista de moedas
                    data = response.json()
                    currencies_list.append(data)
                else:
                    # Se ocorrer um erro na requisição, imprimir o código de status da resposta
                    print(f"Erro ao fazer o request. Código de status: {response.status_code}")

            return currencies_list

    except Exception as Err:
        # Se ocorrer algum erro durante a obtenção das taxas de câmbio, imprimir a mensagem de erro
        print(Err)
