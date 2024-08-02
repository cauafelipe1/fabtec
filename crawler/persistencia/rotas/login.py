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

    if encontrado is None: 
        resposta = jsonify({"resultado": "erro", "detalhes":"usuario ou senha incorreto(s)"})
    else:        
        # criação do Json Web Token (JWT)
        # https://flask-jwt-extended.readthedocs.io/en/3.0.0_release/api/#flask_jwt_extended.create_access_token
        access_token = create_access_token(identity=login)
        # retorno do token
        resposta =  jsonify({"resultado":"ok", "detalhes":access_token})  
 
  return resposta 

''' 
RESULTADOS DE TESTES:

$ curl -X POST localhost:5000/login -d "{\"login\":\"admin@admin.com\",\"senha\":\"admin123\"}" -H "Content-Type: application/json"
{
  "detalhes": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMjYyMTg2NCwianRpIjoiMzYwZTcxMWMtZjQxMi00NTRkLTg2MGYtOGRjMzJlNWQyMDE2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluQGFkbWluLmNvbSIsIm5iZiI6MTcyMjYyMTg2NCwiY3NyZiI6ImVkN2JiZTJhLTE3ODUtNDc1OS04NDI1LTYxYmRhYmZkNzA1NSIsImV4cCI6MTcyMjYyNTQ2NH0.Y_SsS_sft9JXEl9D9Md_dKAI-dS7bl-2En_CGaQ3Vg4",
  "resultado": "ok"
}

$ curl localhost:5000/listar/Usuario -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMjYyMTg2NCwianRpIjoiMzYwZTcxMWMtZjQxMi00NTRkLTg2MGYtOGRjMzJlNWQyMDE2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluQGFkbWluLmNvbSIsIm5iZiI6MTcyMjYyMTg2NCwiY3NyZiI6ImVkN2JiZTJhLTE3ODUtNDc1OS04NDI1LTYxYmRhYmZkNzA1NSIsImV4cCI6MTcyMjYyNTQ2NH0.Y_SsS_sft9JXEl9D9Md_dKAI-dS7bl-2En_CGaQ3Vg4"
{
  "detalhes": [
    {
      "cpf": "00000000000",
      "data de ativacao": "2024-08-02",
      "email": "admin@admin.com",
      "nome": "admin",
      "senha": "eba34065a1d45b3bfd700926b250ee119b42b331977b43b61f6c9d383fcb8f2d898d2b003253796e0eda3a37d3fdffd131758ad348e94dfe9685f787c7911a42",
      "situacao": "ativo",
      "tipo": "admin"
    }
  ],
  "resultado": "ok"
}

$ curl localhost:5000/listar/Consulta -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMjYyMjI4MCwianRpIjoiNGFkZGY4NTItNTcxZS00NWY2LWJjZTMtYzYwMTA1OWM4YTE5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluQGFkbWluLmNvbSIsIm5iZiI6MTcyMjYyMjI4MCwiY3NyZiI6ImE5NDdmNWNiLTM5YmUtNDAwNS1iNjU3LTRlNjc2YjkzYTZhOCIsImV4cCI6MTcyMjYyNTg4MH0.hUw8YUXJs470pxtR-VpvXBQyLe-ew0q7jtxsMYktRE4"
{
  "detalhes": "Cannot load attribute Usuario[1].tipo: the database session is over",
  "resultado": "erro"
}
- não sei porque está ocorrendo este erro, mas no terminal diz:
ERRO: Cannot load attribute Usuario[1].tipo: the database session is over
$ curl -X POST localhost:5000/login -d "{\"login\":\"douglas@gmail.com\",\"senha\":\"douglas123\"}" -H "Content-Type: application/json" 
{
  "detalhes": "usuario ou senha incorreto(s)",
  "resultado": "erro"
}

$ curl localhost:5000/listar/Usuario
{
  "msg": "Missing Authorization Header"
}

$ curl localhost:5000/listar/Consulta
{
  "msg": "Missing Authorization Header"
}

'''