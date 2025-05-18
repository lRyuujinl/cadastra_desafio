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
4. Criar um banco de dados POSTGRESQL:
--------------------------------------------------------------------------------------------------------------------------------------
Usar o comando abaixo para criar o banco de dados da aplicação
CREATE DATABASE CryptoMarket;


--------------------------------------------------------------------------------------------------------------------------------------
5. Passar as configurações de conexão do banco de dados para o arquivo .env (Substituindo os campos necessarios, fora o DB_NAME):
--------------------------------------------------------------------------------------------------------------------------------------
DB_HOST=localhost
DB_NAME=CryptoMarket
DB_USER=postgres
DB_PASSWORD=postgres
DB_PORT=5432


API_CALL_DELAY=1


--------------------------------------------------------------------------------------------------------------------------------------
6. Rodar o script de criação das tabelas no banco de dados:
--------------------------------------------------------------------------------------------------------------------------------------
No terminal dentro do diretorio do projeto, executar:

python db_setup.py

Serão criadas duas tabelas na modelagem de dados pensada:
Tabela 1: `assets` - Guarda dados atuais e mais recentes de cada criptomoeda do mercado

Tabela 2: `asset_history` - Guarda o historico dos dados de preço e dados do mercado (Que será utilizado com mais frequencia para fazer o analytics)


