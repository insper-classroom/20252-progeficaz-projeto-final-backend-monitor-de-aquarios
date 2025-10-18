import pytest
from unittest.mock import patch, MagicMock
from api import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("api.connect_db") # aqui mockamos o connect_db criado dentro do arquivos para fingir que fazemos uma conexao
def test_get_aquarios_disponiveis(mock_connect_db, client):
    # aqui teremos o mock do banco que vamos puxar e em seguida o mock da collection que vamos puxar tambem. fazemos dassa forma pois quando fizermos um find na collection nn fazemos um find no mock e sim um novo mock pra retornar as informações que queremos 
    mock_db = MagicMock()
    mock_collection = MagicMock() 
    # em seguida o resultado que queremos que saia 
    mock_collection.find.return_value = [{
    "id": 1,
    "predio": "predio_1",
    "andar": 1,
    "id_local": 1,
    "capacidade_cadeiras": 10,
    "ocupado": False 
  },
  {
    "id": 2,
    "predio": "predio_1",
    "andar": 1,
    "id_local": 2,
    "capacidade_cadeiras": 6,
    "ocupado": False
  }]

		# essa estrutura diz que quando fizermos colection['algumacoisa'] ele vai retornar o colection que ja checamos 
    mock_db.__getitem__.return_value = mock_collection 
    
    # essa outra estrutura diz que qunado chamarmos o connect_db nos retornamos o nosso mock criado 
    mock_connect_db.return_value = mock_db

		# realizamos a requisição que queremos testar mockando as operações que abordamos anteriormente aqui 
    response = client.get("/aquarios/disponiveis")
		
    assert response.status_code == 200
    assert response.get_json() == { 'aquarios': [
        {
    "id": 1,
    "predio": "predio_1",
    "andar": 1,
    "id_local": 1,
    "capacidade_cadeiras": 10,
    "ocupado": False
  },
  {
    "id": 2,
    "predio": "predio_1",
    "andar": 1,
    "id_local": 2,
    "capacidade_cadeiras": 6,
    "ocupado": False
  }]}