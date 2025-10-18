import pytest
from unittest.mock import patch, MagicMock
from api import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("api.connect_db") # aqui mockamos o connect_db criado dentro do arquivos para fingir que fazemos uma conexao
def test_get_aquario(mock_connect_db, client):
    # aqui teremos o mock do banco que vamos puxar e em seguida o mock da collection que vamos puxar tambem. fazemos dassa forma pois quando fizermos um find na collection nn fazemos um find no mock e sim um novo mock pra retornar as informações que queremos 
    mock_db = MagicMock()
    mock_collection = MagicMock() 
    # em seguida o resultado que queremos que saia usando find_one ao invez de find 
    mock_collection.find_one.return_value = {
        "andar": 1,
        "capacidade_cadeiras": 10,
        "id": 1,
        "id_local": 1,
        "ocupado": True,
        "predio": "predio_1"
    }

		# essa estrutura diz que quando fizermos colection['algumacoisa'] ele vai retornar o colection que ja checamos 
    mock_db.__getitem__.return_value = mock_collection 
    
    # essa outra estrutura diz que qunado chamarmos o connect_db nos retornamos o nosso mock criado 
    mock_connect_db.return_value = mock_db

		# realizamos a requisição que queremos testar mockando as operações que abordamos anteriormente aqui 
    response = client.get("/aquarios/1")
		
    assert response.status_code == 200
    assert response.get_json() == {
    "aquario 1": {
        "andar": 1,
        "capacidade_cadeiras": 10,
        "id": 1,
        "id_local": 1,
        "ocupado": True,
        "predio": "predio_1"
    }
}
    
