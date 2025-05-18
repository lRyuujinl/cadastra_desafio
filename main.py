import time
# import schedule
from db_setup import criar_tabelas
from GetAPIData import API_get_assets, save_to_database

# Orquestrar ordem de execução das funções (Pipeline)
def pipeline():
    print("Iniciando Extração de dados da API")
    
    # Resgatar dados da API
    data = API_get_assets()
    
    # Salvar no banco de dados
    save_to_database(data)
    
    print("Pipeline executada!")

if __name__ == "__main__":
    # Inicio da pipeline com a criação das tabelas:
    criar_tabelas()
    
    # Run once immediately
    pipeline()
    
    # Scheduler para a necessidade de atualização recorrente dos dados - Apenas descomentar o bloco de codigo abaixo

    # schedule.every(1).hour.do(pipeline)
    # print("Scheduled to run hourly. Press Ctrl+C to exit.")
    # try:
    #     while True:
    #         schedule.run_pending()
    #         time.sleep(60)
    # except KeyboardInterrupt:
    #     print("Pipeline stopped")