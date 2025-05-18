import psycopg2
from config import DB_CONFIG

def criar_tabelas():

    # Queries para criação de tabelas:
    query_tb_assets = """
        CREATE TABLE IF NOT EXISTS assets (
            id VARCHAR(50) PRIMARY KEY,
            rank INTEGER,
            symbol VARCHAR(10),
            name VARCHAR(100),
            supply NUMERIC,
            max_supply NUMERIC,
            market_cap_usd NUMERIC,
            volume_usd_24hr NUMERIC,
            price_usd NUMERIC,
            change_percent_24hr NUMERIC,
            vwap_24hr NUMERIC,
            updated_at TIMESTAMP
        )
    """
    
    
    query_tb_asset_history = """  
        CREATE TABLE IF NOT EXISTS asset_history (
            id SERIAL PRIMARY KEY,
            asset_id VARCHAR(50) REFERENCES assets(id),
            price_usd NUMERIC,
            market_cap_usd NUMERIC,
            volume_usd_24hr NUMERIC,
            timestamp TIMESTAMP
        )
        """
    
    conn = None

    try:
        # Conectar banco de dados + cursor para operações
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Criar tabelas
        cur.execute(query_tb_assets)
        cur.execute(query_tb_asset_history)
        cur.close()
        conn.commit()
        
        print("Tabelas criadas com sucesso!")
    
    # Tratamento de Erros para caso ocorra algo
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    criar_tabelas()