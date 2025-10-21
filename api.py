from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from pymongo import MongoClient
from dotenv import load_dotenv


# ==========================================Funções implementadas nessa api ==================================================

# - connect_db(): conecta ao banco MongoDB e retorna o objeto db.
# - get_aquarios(): retorna todos os aquários cadastrados.
# - get_aquario(id_aquario): retorna um aquário específico pelo ID.
# - get_aquarios_disponiveis(): lista apenas os aquários desocupados.
# - update_ocupacao(id): alterna o estado de ocupação (True/False) de um aquário.
# - filter() : filtra os aquarios com base no arg da request 


load_dotenv('.cred') # aqui carregamos o arquivo .cred temporariamente na sessão

mongo_uri = os.getenv('MONGO_URI')  #leitura das credenciais do banco 
db_name = os.getenv('DB_NAME')

def connect_db():
    try:
        client = MongoClient(mongo_uri)
        db = client[db_name]
        return db
    except Exception as e:
        print(f"Erro ao conectar ao MongoDB: {e}")
        return None



app = Flask(__name__)
CORS(app)

@app.route('/aquarios', methods=['GET'])
def get_aquarios():
    db = connect_db()
    if db is None:
        return {"erro": "Erro ao conectar ao banco de dados"}, 500

    try:
        collection = db['aquarios']
        aquarios_cursor = collection.find({}, {"_id": 0})   # Remove o campo _id da resposta pra tornar o objeto possivel de se serializar 
        aquarios = list(aquarios_cursor)

        if not aquarios:
            return {"erro": "Nenhum aquario encontrado"}, 404
        return {"aquarios": aquarios}, 200
    except Exception as e:
        return {"erro": f"Erro ao consultar aquarios: {str(e)}"}, 500


@app.route('/aquarios/<int:id_aquario>', methods = ['GET'])

def get_aquario(id_aquario):
    db = connect_db()
    if db is None:
      return {"erro": "Erro ao conectar ao banco de dados"}, 500
      
    try:
        collection = db['aquarios']
        aquarios_cursor = collection.find_one({"id" : id_aquario}, {"_id": 0}) 
        if not aquarios_cursor:
            return {'error':'aquario não encontrado'}, 404
        else:
            return {f'aquario {id_aquario}':aquarios_cursor}
        

    except Exception as e:
        return {"erro": f"erro ao encontrar aquario {e}"},500
    
@app.route('/aquarios/<int:id>', methods = ['PUT'])

def update_ocupacao(id):
    db = connect_db()
    if db is None:
      return {"erro": "Erro ao conectar ao banco de dados"}, 500
    try:
        collection = db['aquarios']
        aquario = collection.find_one({"id":id}, {"_id": 0})  # procuramos o aquario 
        
				# se ele estiver ocupado trocamos para false e se estiver livre trocamos pra true 
        if aquario['ocupado'] == True:
            collection.update_one({"id" : id}, {"$set":{"ocupado": False}})
            return {'mensagem':'estado de ocupacao alterado'},200
        elif aquario['ocupado'] == False:
            collection.update_one({"id" : id}, {"$set":{"ocupado": True}})
            return {'mensagem':'estado de ocupacao alterado'},200            
        if not aquario:
            return {'mensagem':'nenhum aquario encontrado'}, 404
        
    except Exception as e:
        return {"erro": "erro ao atualizar ocupação do aquario {e}"},500    



@app.route('/aquarios/filter', methods = ['GET']) #passo os filtros por meio de parametros
def filter():
    db = connect_db()
    if db is None:
        return {"Erro":"Erro ao conectar com o banco de dados"}
    else:
        collection = db['aquarios']
        predio = request.args.get("predio")# recebo os parametros aqui
        andar = request.args.get("andar")
        capacidade = request.args.get("capacidade")
        ocupacao = request.args.get("ocupacao")
        
        filtros = {}#coloco todos os parametros nesse dicionario caso venham 
        if predio and predio != "None":
            filtros["predio"]= str(predio)
            
        if andar and andar != "None":
            filtros["andar"]= int(andar)
            
        if capacidade and capacidade != "None":
            filtros["capacidade"]= int(capacidade)
            
        if ocupacao and ocupacao != "None":
            filtros["ocupacao"]= bool(ocupacao)
        
        try:
            aquarios_cursor = collection.find(filtros, {"_id": 0})# uso aquele dicionario para estipular os filtros
            aquarios = list(aquarios_cursor)# transformo o cursor em lista para puder passar em json
            if not aquarios:
                return {"erro": "Nenhum aquário encontrado"}, 404
            
            if andar and andar != "None" and (predio == 'None' or not predio):
                return {"erro": "Selecione um prédio"}, 500

            return {"aquarios": aquarios}, 200

        except Exception as e:
            return {"erro": f"Erro ao consultar aquários: {str(e)}"}, 500


            
if __name__ == '__main__':
    app.run(debug=True)