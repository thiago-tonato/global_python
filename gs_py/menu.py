import json
import requests
import pandas as pd
from datetime import datetime

# Função para validar data no formato YYYY-MM-DD
def validar_entrada_data(data):
    try:
        datetime.strptime(data, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Função para validar valores numéricos positivos
def validar_valor_positivo(valor):
    try:
        valor = float(valor)
        return valor > 0
    except ValueError:
        return False

# Função para exportar residências para JSON
def exportar_residencias_para_json(residencias):
    try:
        with open('residencias_exportadas.json', 'w') as f:
            json.dump(residencias, f, indent=4)
        print("Dados exportados para JSON com sucesso.")
    except Exception as e:
        print(f"Erro ao exportar para JSON: {e}")

# Função para exportar residências para Excel
def exportar_residencias_para_excel(residencias):
    try:
        df = pd.DataFrame(residencias, columns=["id_residencia", "nome_responsavel", "endereco", "capacidade_geracao", "tipo_fonte", "limite_consumo", "data_cadastro"])
        df.to_excel('residencias_exportadas.xlsx', index=False)
        print("Dados exportados para Excel com sucesso.")
    except Exception as e:
        print(f"Erro ao exportar para Excel: {e}")

# Função para adicionar uma residência
def adicionar_residencia_interativo():
    print("Adicionar nova residência:")
    nome_responsavel = input("Nome do responsável: ")
    endereco = input("Endereço: ")
    capacidade_geracao = input("Capacidade de geração (kWh): ")
    tipo_fonte = input("Tipo de fonte (ex: Solar, Eólica): ")
    limite_consumo = input("Limite de consumo (kWh): ")
    
    if not capacidade_geracao.isnumeric() or not limite_consumo.isnumeric():
        print("Capacidade de geração e limite de consumo devem ser valores válidos.")
        return
    
    payload = {
        "nome_responsavel": nome_responsavel,
        "endereco": endereco,
        "capacidade_geracao": capacidade_geracao,
        "tipo_fonte": tipo_fonte,
        "limite_consumo": limite_consumo
    }
    
    try:
        response = requests.post("http://localhost:5000/residencias", json=payload)
        if response.status_code == 200:
            print(response.json().get("message", "Residência adicionada com sucesso!"))
        else:
            print(f"Erro ao adicionar residência: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão com o servidor: {e}")

# Função para adicionar histórico de energia
def adicionar_historico_interativo():
    print("Adicionar novo histórico de energia:")
    id_residencia = input("ID da residência: ")
    data_registro = input("Data de registro (YYYY-MM-DD): ")
    producao = input("Produção de energia (kWh): ")
    consumo = input("Consumo de energia (kWh): ")
    
    if not producao.isnumeric() or not consumo.isnumeric():
        print("Produção e consumo de energia devem ser valores válidos.")
        return

    if not validar_entrada_data(data_registro):
        print("Data de registro inválida. Use o formato YYYY-MM-DD.")
        return
    
    payload = {
        "id_residencia": id_residencia,
        "data_registro": data_registro,
        "producao": producao,
        "consumo": consumo
    }
    
    try:
        response = requests.post("http://localhost:5000/historico", json=payload)
        if response.status_code == 200:
            print(response.json().get("message", "Histórico de energia adicionado com sucesso!"))
        else:
            print(f"Erro ao adicionar histórico: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão com o servidor: {e}")

# Função para consultar residências
def consultar_residencias_interativo():
    tipo_fonte = input("Tipo de fonte para filtro (deixe em branco para todos): ")
    limite_consumo_min = input("Limite de consumo mínimo (deixe em branco para todos): ")

    params = {"tipo_fonte": tipo_fonte}

    if limite_consumo_min != "":
        try:
            limite_consumo_min = float(limite_consumo_min)
            if limite_consumo_min <= 0:
                print("Limite de consumo mínimo deve ser um valor positivo.")
                return
            params["limite_consumo_min"] = limite_consumo_min
        except ValueError:
            print("Limite de consumo mínimo deve ser um número.")
            return
    
    try:
        response = requests.get("http://localhost:5000/residencias/consultar", params=params)
        if response.status_code == 200:
            residencias = response.json()
            print(json.dumps(residencias, indent=4))

            # Pergunta se o usuário deseja exportar
            escolha_exportar = input("Deseja exportar os dados? (1 - JSON, 2 - Excel, 3 - Não): ")
            if escolha_exportar == "1":
                exportar_residencias_para_json(residencias)
            elif escolha_exportar == "2":
                exportar_residencias_para_excel(residencias)
        else:
            print(f"Erro na consulta: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão com o servidor: {e}")

# Função para exportar dados
def exportar_dados():
    escolha = input("Deseja exportar os dados para JSON (1) ou Excel (2)? ")
    if escolha == "1":
        try:
            response = requests.get("http://localhost:5000/residencias/consultar")
            if response.status_code == 200:
                exportar_residencias_para_json(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão com o servidor: {e}")
    elif escolha == "2":
        try:
            response = requests.get("http://localhost:5000/residencias/consultar")
            if response.status_code == 200:
                exportar_residencias_para_excel(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão com o servidor: {e}")
    else:
        print("Opção inválida.")

def menu():
    while True:
        print("\nMenu de Opções:")
        print("1 - Adicionar residência")
        print("2 - Adicionar histórico de energia")
        print("3 - Consultar residências")
        print("4 - Exportar dados")
        print("5 - Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            adicionar_residencia_interativo()
        elif opcao == "2":
            adicionar_historico_interativo()
        elif opcao == "3":
            consultar_residencias_interativo()
        elif opcao == "4":
            exportar_dados()
        elif opcao == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == '__main__':
    menu()
