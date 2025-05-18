import os
from dotenv import load_dotenv

# Carregar configurações de conexão:
load_dotenv()

#POSTGRESQL
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'CryptoMarket'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres'),
    'port': os.getenv('DB_PORT', '5432')
}

# API (Especificamente Assets apenas)
API_URL = 'https://rest.coincap.io/v3/assets'

PARAMS = {
    'apiKey': '204fc30883ecd238f97765faf486871ef2453a627c0efcde823f4c416952a3a9',
    'limit': 10
}