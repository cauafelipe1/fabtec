from geral.config import *
from geral.cripto import *
from modelo.usuario import *

# login para a obtenção do token
@app.route("/login", methods=['POST'])
def login():
  
  #coleta os dados fornecidos pelo curl
  dados = request.get_json()
  login = dados['login']
  senha = dados['senha']

  # verfica se os dados fornecidos no curl são os mesmos do banco de dados
  with db_session:
    encontrado = Usuario.get(email=login, senha=cifrar(senha))
    tipo = encontrado.tipo
    if encontrado is None: 
        resposta = jsonify({"resultado": "erro", "detalhes":"usuario ou senha incorreto(s)"})
    else:
        # criação do Json Web Token (JWT)
        # https://flask-jwt-extended.readthedocs.io/en/3.0.0_release/api/#flask_jwt_extended.create_access_token
        if encontrado.data_ativacao is not None:
          ativo = encontrado.data_ativacao
          access_token = create_access_token(identity={"email": login, "tipo": tipo})
          # retorno do token
          resposta =  jsonify({"resultado":"ok", "detalhes":access_token}) 
        else:
           resposta =  jsonify({"resultado":"erro", "detalhes":"acesso bloqueado! seu usuario esta inativo"}) 
 
  return resposta 

''' 
RESULTADOS DE TESTES:

$ curl -X POST localhost:5000/login -d "{\"login\":\"admin@admin.com\",\"senha\":\"admin123\"}" -H "Content-Type: application/json"
{
  "detalhes": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMzEyOTI1MywianRpIjoiMGJiNmUzNzktNmQ4YS00OGFmLThkZGUtYzIxNWZmNTgxMTI5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsInRpcG8iOiJhZG1pbiJ9LCJuYmYiOjE3MjMxMjkyNTMsImNzcmYiOiJlMzM5MmE3MC03ODRmLTQ3NDAtODg5My1hZjRmNTU5ODE0MGUiLCJleHAiOjE3MjMxMzI4NTN9.GgoMpu7N8ay_DrO68Wmygt955RUIhi8XwWK5teejANQ",
  "resultado": "ok"
}

$ curl -X POST localhost:5000/login -d "{\"login\":\"douglas@gmail.com\",\"senha\":\"douglas123\"}" -H "Content-Type: application/json" 
{
  "detalhes": "usuario ou senha incorreto(s)",
  "resultado": "erro"
}

curl -X POST localhost:5000/login -d "{\"login\":\"juniorsales@gmail.com\",\"senha\":\"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMzE0MzQwNCwianRpIjoiMDRkODU1YjEtYWE3NC00N2ZkLWI4ZjAtNWRlOWVkYzRmODY4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imp1bmlvcnNhbGVzQGdtYWlsLmNvbSIsIm5iZiI6MTcyMzE0MzQwNCwiY3NyZiI6IjkxMzcxNTRiLWNhN2ItNGM0OS1iODZmLWM4MWVjOWZlODYwYiIsImV4cCI6MTcyMzE0NzAwNH0.BkgWFXyZkUyTiHGzBj7qFVAP1fmMxtv68QUAGex2HSE\"}" -H "Content-Type: application/json"
{
  "detalhes": "acesso bloqueado! seu usuario esta inativo",
  "resultado": "erro"
}
'''