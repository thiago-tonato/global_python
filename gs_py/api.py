import json
import pandas as pd
from flask import Flask, request, jsonify
from database import Database

app = Flask(__name__)

# Função para exportar residências para JSON
def exportar_residencias_para_json():
    db = Database()
    try:
        sql = "SELECT * FROM residencias"
        result = db.query(sql)
        if result:
            with open('residencias_exportadas.json', 'w') as f:
                json.dump(result, f, indent=4)
            print("Dados exportados com sucesso para 'residencias_exportadas.json'.")
        else:
            print("Nenhuma residência encontrada para exportação.")
    except Exception as e:
        print(f"Erro ao exportar dados: {e}")
    finally:
        db.close()

# Função para exportar residências para Excel
def exportar_residencias_para_excel():
    db = Database()
    try:
        sql = "SELECT * FROM residencias"
        result = db.query(sql)
        if result:
            df = pd.DataFrame(result, columns=["id_residencia", "nome_responsavel", "endereco", "capacidade_geracao", "tipo_fonte", "limite_consumo", "data_cadastro"])
            df.to_excel('residencias_exportadas.xlsx', index=False)
            print("Dados exportados com sucesso para 'residencias_exportadas.xlsx'.")
        else:
            print("Nenhuma residência encontrada para exportação.")
    except Exception as e:
        print(f"Erro ao exportar dados: {e}")
    finally:
        db.close()

# Função para adicionar residência
@app.route('/residencias', methods=['POST'])
def adicionar_residencia():
    data = request.get_json()

    db = Database()
    try:
        sql = """
        INSERT INTO residencias (id_residencia, nome_responsavel, endereco, capacidade_geracao, tipo_fonte, limite_consumo)
        VALUES (residencia_seq.NEXTVAL, :nome_responsavel, :endereco, :capacidade_geracao, :tipo_fonte, :limite_consumo)
        """
        db.execute(sql, {
            "nome_responsavel": data["nome_responsavel"],
            "endereco": data["endereco"],
            "capacidade_geracao": data["capacidade_geracao"],
            "tipo_fonte": data["tipo_fonte"],
            "limite_consumo": data["limite_consumo"]
        })
        return jsonify({"message": "Residência adicionada com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# Função para consultar residências com filtros
@app.route('/residencias/consultar', methods=['GET'])
def consultar_residencias():
    tipo_fonte = request.args.get('tipo_fonte', '')
    limite_consumo_min = request.args.get('limite_consumo_min', 0)

    db = Database()
    try:
        sql = """
        SELECT * FROM residencias
        WHERE tipo_fonte LIKE :tipo_fonte
        AND limite_consumo >= :limite_consumo_min
        """
        result = db.query(sql, {"tipo_fonte": f"%{tipo_fonte}%", "limite_consumo_min": limite_consumo_min})
        
        if result:
            return jsonify(result), 200
        else:
            return jsonify({"message": "Nenhuma residência encontrada com os filtros aplicados."}), 404
    finally:
        db.close()

# Função para adicionar histórico de energia
@app.route('/historico', methods=['POST'])
def adicionar_historico():
    data = request.get_json()

    saldo_energetico = data['producao'] - data['consumo']
    
    db = Database()
    try:
        sql = """
        INSERT INTO historico_energia (id_historico, id_residencia, data_registro, producao, consumo, saldo_energetico)
        VALUES (historico_seq.NEXTVAL, :id_residencia, TO_DATE(:data_registro, 'YYYY-MM-DD'), :producao, :consumo, :saldo_energetico)
        """
        db.execute(sql, {
            "id_residencia": data["id_residencia"],
            "data_registro": data["data_registro"],
            "producao": data["producao"],
            "consumo": data["consumo"],
            "saldo_energetico": saldo_energetico
        })
        return jsonify({"message": "Histórico de energia adicionado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
