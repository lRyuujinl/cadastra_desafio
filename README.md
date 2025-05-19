# cadastra_desafio

# cadastra_desafio

Para utilizar o codigo nesse repositório, serão necessários os seguintes passos:
--------------------------------------------------------------------------------------------------------------------------------------
1. Clonar o repositorio para uma pasta chamado CRYPTOMARKET
--------------------------------------------------------------------------------------------------------------------------------------
Os arquivos que serão clonados são definidos como:
a. config.py            # Configurações de conexão da API e do banco de dados
b. db_setup.py          # Criação das tabelas que vao ser usadas no programa
c. GetAPIData.py        # Responsavel por puxar os dados da API e inserir no banco de dados criado
d. main.py              # Script que junta todas as peças, executa e orquestra a pipeline (Esse arquivo será usado para executar)
e. dependencias.txt     # Todas as bibliotecas que precisam ser instaladas para o script funcionar
f. .env                 # Arquivo contendo as autenticações para conectar a um banco de dados (Normalmente eu não subiria esse arquivo, mas por motivos de desafio, subi rs)


--------------------------------------------------------------------------------------------------------------------------------------
2. Criar um ambiente virtual para rodar a aplicação
--------------------------------------------------------------------------------------------------------------------------------------
Rodar no Prompt de comando do Windows:
python -m venv venv

venv\Scripts\activate

Ou se usar Mac/Linux:
source venv/bin/activate


--------------------------------------------------------------------------------------------------------------------------------------
3. Instalar as dependencias para poder usar as bibliotecas no script
--------------------------------------------------------------------------------------------------------------------------------------
Rodar no Terminal: 
pip install -r requirements.txt


--------------------------------------------------------------------------------------------------------------------------------------
4. Adicionar uma chave de autenticação da API no config.py
--------------------------------------------------------------------------------------------------------------------------------------
Para que a API funcione, o serviço requer uma chave valida. (No caso, deixei uma chave que ainda permite que seja feita a coleta de dados).
Mas caso deseje usar uma outra chave, insira a nova dentro do campo `apiKey`. 

(Nota: Optei por deixar os parametros fora do env mesmo, mas é uma opção inserir também dentro do .env por questão de segurança)


--------------------------------------------------------------------------------------------------------------------------------------
5. Criar um banco de dados POSTGRESQL:
--------------------------------------------------------------------------------------------------------------------------------------
Usar o comando abaixo para criar o banco de dados da aplicação
CREATE DATABASE CryptoMarket;


--------------------------------------------------------------------------------------------------------------------------------------
6. Passar as configurações de conexão do banco de dados para o arquivo .env (Substituindo os campos necessarios, fora o DB_NAME):
--------------------------------------------------------------------------------------------------------------------------------------
DB_HOST=localhost
DB_NAME=CryptoMarket
DB_USER=postgres
DB_PASSWORD=postgres
DB_PORT=5432


API_CALL_DELAY=1


--------------------------------------------------------------------------------------------------------------------------------------
7. Rodar o script de criação das tabelas no banco de dados:
--------------------------------------------------------------------------------------------------------------------------------------
No terminal dentro do diretorio do projeto, executar:

python db_setup.py

Serão criadas duas tabelas na modelagem de dados pensada:
Tabela 1: `assets` - Guarda dados atuais e mais recentes de cada criptomoeda do mercado

Tabela 2: `asset_history` - Guarda o historico dos dados de preço e dados do mercado (Que será utilizado com mais frequencia para fazer o analytics)


--------------------------------------------------------------------------------------------------------------------------------------
8. Rodar a aplicação principal
--------------------------------------------------------------------------------------------------------------------------------------
Rodar no terminal o seguinte comando:

python main.py

Esse é o comando principal da aplicação, que fará a chamada da API e armazenar o resultado nas duas tabelas do banco de dados criado e que estará configurado por padrão a rodar a cada hora.

Mas é possível optar também pela execução manual da chamada da API sem o scheduler com o comando:

pyhton GetAPIData.py


--------------------------------------------------------------------------------------------------------------------------------------
9. Conectando ao Looker Studio
--------------------------------------------------------------------------------------------------------------------------------------
Como o banco de dados utilizado é local, é necessário configurar o PostgreSQL para aceitar conexoes remotas, ou redirecionar a porta de acesso, ou usar um banco de dados já em Cloud.

Essencialmente, assim que o banco de dados estiver acessivel na rede:

A. Acesse lookerstudio.google.com
B. Clique em "Criar" e selecione "Fonte de dados"
C. Role para baixo até os conectores de "Banco de dados" e selecione "PostgreSQL"
D. Insira seus detalhes de conexão:
E. Nome do host/IP
F. Porta (padrão 5432)
G. Nome do banco de dados
H. Nome de usuário e senha
I. Teste a conexão e clique em "Conectar"


--------------------------------------------------------------------------------------------------------------------------------------
10. Criando as visualizações do Dash:
--------------------------------------------------------------------------------------------------------------------------------------
Como os dados já estão tratados e estão utilizaveis, não há por enquanto a necessidade de fazer algumas transformações para algo mais estruturado, sendo possivel realizar algumas análises mais diretas e uteis como:

1. Entender quais são as 10 principais moedas mais valorizadas atualmente no mercado

Query:

SELECT name, symbol, price_usd, market_cap_usd 
FROM assets 
ORDER BY market_cap_usd DESC 
LIMIT 10


2. Estudar o comportamento do historico de preço de todas, ou alguma moeda especificamente:
Query:

SELECT a.name
    , h.timestamp
    , h.price_usd 

FROM asset_history h

LEFT JOIN assets a 
    ON h.asset_id = a.id

-- Filtro de moedas se precisar, ou fazer o filtro direto pelo Looker studio puxando um filter box das opções no dash
WHERE a.symbol IN ('BTC', 'ETH', 'XRP')

ORDER BY h.timestamp


--------------------------------------------------------------------------------------------------------------------------------------
10. Observações:
--------------------------------------------------------------------------------------------------------------------------------------
Dado que a API já devolve dados relativamente bem tratados e transformados, não houve a necessidade de fazer mais limpeza ou transformação, tirando a questão dos metadados e a tipagem de cada dado.

Caso os dados fossem mais transacionais e "crús", eu utilizaria esse script para puxar os dados puros para um Data Lake e a partir dali, criar uma Data Warehouse e gerenciar todas as transformações e agregações de dados usando Stored Procedures ao invés de fazer usando as bibliotecas no Python, criando as zonas de Raw, Treated, Trusted e Refined dos dados para permitir a criação de dashboards mais otimizados e organizados também.
