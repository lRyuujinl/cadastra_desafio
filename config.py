import os
from dotenv import load_dotenv

# Carregar configurações de conexão:
load_dotenv()

#POSTGRESQL
DB_CONFIG = {
    'host': os.getenv('DB_HOST', ''),
    'database': os.getenv('DB_NAME', ''),
    'user': os.getenv('DB_USER', ''),
    'password': os.getenv('DB_PASSWORD', ''),
    'port': os.getenv('DB_PORT', '')
}

# API (Especificamente Assets apenas)
API_URL = 'https://rest.coincap.io/v3/assets'

PARAMS = {
    'apiKey': '204fc30883ecd238f97765faf486871ef2453a627c0efcde823f4c416952a3a9',
    'limit': 300
}

# Pela documentação, o limite é de 600 calls por minuto, portanto, para não extrapolar, é possivel usar um timer para controlar a vazão de chamadas
API_CALL_DELAY = int(os.getenv('API_CALL_DELAY', ''))