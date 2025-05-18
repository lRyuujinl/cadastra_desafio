import requests
import psycopg2
import datetime
from config import DB_CONFIG, API_URL, PARAMS

def API_get_assets():
    """Request da API """
    try:
        response = requests.get(API_URL, params=PARAMS)
        response.raise_for_status()  # Tratamento de Erros
        
        # Converte Request em Json
        data = response.json()
        return data.get('data', [])
    
    #Tratamento de eventuais erros
    except requests.exceptions.RequestException as e:
        print(f"Erro ao tentar fazer uma chamada pela API: {e}")
        return []

#Salvar dados da Request em um banco de dados PostgreSQL
def save_to_database(crypto_data):
    if not crypto_data:
        print("Não há dados para serem salvos")
        return
    
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Current timestamp
        current_time = datetime.datetime.now()
        
        # UPSERT (Para não correr o risco de salvar duplicados)
        for asset in crypto_data:
            # Converte dados dtype object do Json nos tipos correspondentes do SQL 
            asset_id = asset.get('id')
            rank = int(asset.get('rank', 0))
            symbol = asset.get('symbol')
            name = asset.get('name')
            supply = float(asset.get('supply', 0)) if asset.get('supply') else None
            max_supply = float(asset.get('maxSupply', 0)) if asset.get('maxSupply') else None
            market_cap_usd = float(asset.get('marketCapUsd', 0)) if asset.get('marketCapUsd') else None
            volume_usd_24hr = float(asset.get('volumeUsd24Hr', 0)) if asset.get('volumeUsd24Hr') else None
            price_usd = float(asset.get('priceUsd', 0)) if asset.get('priceUsd') else None
            change_percent_24hr = float(asset.get('changePercent24Hr', 0)) if asset.get('changePercent24Hr') else None
            vwap_24hr = float(asset.get('vwap24Hr', 0)) if asset.get('vwap24Hr') else None
            
            cur.execute("""
                INSERT INTO assets (
                    id, rank, symbol, name, supply, max_supply, market_cap_usd, 
                    volume_usd_24hr, price_usd, change_percent_24hr, vwap_24hr, updated_at
                ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) 
                DO UPDATE SET 
                    rank = EXCLUDED.rank,
                    symbol = EXCLUDED.symbol,
                    name = EXCLUDED.name,
                    supply = EXCLUDED.supply,
                    max_supply = EXCLUDED.max_supply,
                    market_cap_usd = EXCLUDED.market_cap_usd,
                    volume_usd_24hr = EXCLUDED.volume_usd_24hr,
                    price_usd = EXCLUDED.price_usd,
                    change_percent_24hr = EXCLUDED.change_percent_24hr,
                    vwap_24hr = EXCLUDED.vwap_24hr,
                    updated_at = EXCLUDED.updated_at
            """, (
                asset_id, rank, symbol, name, supply, max_supply, market_cap_usd,
                volume_usd_24hr, price_usd, change_percent_24hr, vwap_24hr, current_time
            ))
            
            # Inserção simples na tabela de histórico
            try:
                cur.execute("""
                    INSERT INTO asset_history (
                        asset_id, price_usd, market_cap_usd, volume_usd_24hr, timestamp
                    )
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    asset_id, price_usd, market_cap_usd, volume_usd_24hr, current_time
                ))
            except psycopg2.errors.UniqueViolation:
                # Se já existir um registro para este asset_id e timestamp, ignoramos
                conn.rollback()  # Rollback apenas desta operação
                continue
        
        # Commit the transaction
        conn.commit()
        print(f"Foram inseridos/atualizados dados de {len(crypto_data)} moedas!")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao executar a transação: {error}")
        if conn:
            # Tratamento de erro com rollback para manter consistência das transações
            conn.rollback()
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    data = API_get_assets()
    save_to_database(data)