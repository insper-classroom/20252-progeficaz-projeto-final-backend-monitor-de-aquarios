from flask import Flask, request, jsonify
import os
from pymongo import MongoClient
from dotenv import load_dotenv

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
        
        
@app.route('/aquarios/disponiveis', methods=['GET'])

def get_aquarios_disponiveis():
    db = connect_db()
    if db is None:
      return {"erro": "Erro ao conectar ao banco de dados"}, 500
    
    try:
        collection = db['aquarios']
        aquarios_cursor = collection.find({"ocupado" : False}, {"_id": 0})  #procura todos os aquarios que tem false na categoria ocupado
        if not aquarios_cursor:
            return {'mensagem':'nenhum aquario livre'}, 404
        else:
            return {'aquarios':aquarios_cursor}, 200
        

    except Exception as e:
        return {"erro": "erro ao encontrar aquarios livres {e}"},500
    
@app.route('/aquarios/<int:id>/update_ocupacao', methods = ['PUT'])

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
    
if __name__ == '__main__':
    app.run(debug=True)