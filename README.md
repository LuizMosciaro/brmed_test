# Como executar o projeto em uma máquina local
## Configurando as variáveis de ambiente.
- Clone o arquivo ```.env.example``` com o nome de ```.env```
- Preencha todas as variáveis
- - A variável ```SECRET_KEY``` pode ser gerada em [djecrety](https://djecrety.ir/).
- - A variável ```DEBUG``` pode ser inicializada como ```TRUE``` para ver os relatórios de erros, ou ```FALSE``` para ignorar.
- - A variável ```ALLOWED_HOSTS``` é uma lista de hosts autorizados e pode ser inicializada com ``localhost,127.0.0.1,0.0.0.0``.


# Desafio  proposto pela empresa:
Segue a história de usuário:

Preciso de um sistema que guarde as cotações do dólar versus real, 
euro e iene(JPY) e que as exibe em um gráfico, respeitando as seguintes especificações:

* Deve ser possível informar uma data de início e de fim para consultar qualquer período 
    de tempo, contanto que a diferenca entre o inicio e fim do período informado
    seja de no máximo 5 dias úteis.
* Deve ser possível variar as moedas (real, euro e iene).

Existem algumas restrições que devem ser seguidas:
* Os dados das cotações devem ser coletados utilizando 
    a api do https://www.vatcomply.com/documentation (Você vai precisar usar Dólar como base).
* O código deve ser desenvolvido utilizando um repositório git no seu perfil do Github ou BitBucket;
* Backend: deve ser implementado em python utilizando o framework django.
* Frontend: o único requisito é usar o highcharts para apresentação dos dados.
* Não precisa de login, usuário, autenticação ou qualquer coisa. Só a página carregando o gráfico.


O que será avaliado?
* Clareza do código escrito.
* Uso de Orientação a Objetos.
* Entendimento de práticas de desenvolvimento como testes automatizados, utilização correta do controle de versão.
* Conhecimento do framework escolhido.


Bônus:
* Deploy no heroku ou em outro servidor de sua preferência.
* Criar uma api para realizar leitura das cotações persistidas no banco de dados.

