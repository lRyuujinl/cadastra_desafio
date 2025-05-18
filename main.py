import time
import sys
# import schedule
from db_setup import criar_tabelas
from GetAPIData import API_get_assets, save_to_database

# Orquestrar ordem de execução das funções (Pipeline)
def pipeline():
    print("Iniciando Extração de dados da API")
    
    try:
        print("Rodando serviço da API:")
        data = API_get_assets()
        
        if not data:
            print("Interrompendo a API por causa de um erro no serviço.")
            return False
        
        print("Dados puxados da API com sucesso!")
        
        print("Salvando dados no banco de dados...")
        save_to_database(data)

        print("Dados salvos com sucesso.")
        return True

    except Exception as e:
        print(f"Erro durante a execução da pipeline - {e}")
        print("Parando a Pipeline")
        return False    
    
if __name__ == "__main__":
   try:
        # Inicio da pipeline com a criação das tabelas:
        criar_tabelas()
   except Exception as e:
        print(f"Erro ao criar as tabelas - {e}")
        print("Parando a criação devido ao erro.")
        sys.exit(1)
    
    # 
   tentativa = pipeline()
   
   if not tentativa:
        print("Erro ao tentar executar a pipeline, cancelando a operação")
        sys.exit(1)    
    
    # Scheduler para a necessidade de atualização recorrente dos dados - Apenas descomentar o bloco de codigo abaixo

    # schedule.every(1).hour.do(pipeline)
    # print("Scheduled to run hourly. Press Ctrl+C to exit.")
    # try:
    #     while True:
    #         schedule.run_pending()
    #         time.sleep(60)
    # except KeyboardInterrupt:
    #     print("Pipeline stopped")