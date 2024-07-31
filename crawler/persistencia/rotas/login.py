from geral.config import *
from geral.cripto import *
from modelo.usuario import *

#login para a obtenção do token
@app.route("/login", methods=['POST'])
def login():
  
  #coleta os dados fornecidos pelo curl
  dados = request.get_json()
  login = dados['login']
  senha = dados['senha']

  #verfica se os dados fornecidos no curl são os mesmos da tabela
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

$ curl -X POST localhost:5000/login -d "{\"login\":\"douglas@gmail.com\",\"senha\":\"12345678\"}" -H "Content-Type: application/json"
{
  "detalhes": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMTk3MDQwNiwianRpIjoiZTFhYTQ0M2UtNWI3MC00MjViLWJlYTEtOWNmMTkzOWExN2Y2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImRvdWdsYXNAZ21haWwuY29tIiwibmJmIjoxNzIxOTcwNDA2LCJjc3JmIjoiMjJlOTQ2NDAtNjE2NS00YzU1LTlhM2UtNTEwN2JhOTk4NzQ2IiwiZXhwIjoxNzIxOTc0MDA2fQ.AxHG99mbvujq8DGe1Yn-XNZivNbT7wCFd2br-X1UsAY",
  "resultado": "ok"
}

$ curl localhost:5000/listar/Pessoa -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMTk3MDQwNiwianRpIjoiZTFhYTQ0M2UtNWI3MC00MjViLWJlYTEtOWNmMTkzOWExN2Y2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImRvdWdsYXNAZ21haWwuY29tIiwibmJmIjoxNzIxOTcwNDA2LCJjc3JmIjoiMjJlOTQ2NDAtNjE2NS00YzU1LTlhM2UtNTEwN2JhOTk4NzQ2IiwiZXhwIjoxNzIxOTc0MDA2fQ.AxHG99mbvujq8DGe1Yn-XNZivNbT7wCFd2br-X1UsAY"
{
  "detalhes": [
    {
      "cpf": "12345678901",
      "email": "douglas@gmail.com",
      "nome": "douglas",
      "senha": "f5560c3296de4e0ef868574bf96fc778bc580931a8cae2d2631de27ba055db1be2afd769d658c684d8bc5ee0c1b2a7583ec862d5e994b806c6fa2ab4d54cd7f4"
    },
    {
      "cpf": "11111111111",
      "email": "hugo@gmail.com",
      "nome": "hugo",
      "senha": "629bc9ef82140705ecc6bca4745d5b0cc169e4e97a14b9aeaad37563b22272eb30068e9fa8d7c597586182647495b4405150e4489e6756b35603022395cb3ad9"
    }
  ],
  "resultado": "ok"
}

$ curl localhost:5000/listar/Consulta -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMTk3MDQwNiwianRpIjoiZTFhYTQ0M2UtNWI3MC00MjViLWJlYTEtOWNmMTkzOWExN2Y2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImRvdWdsYXNAZ21haWwuY29tIiwibmJmIjoxNzIxOTcwNDA2LCJjc3JmIjoiMjJlOTQ2NDAtNjE2NS00YzU1LTlhM2UtNTEwN2JhOTk4NzQ2IiwiZXhwIjoxNzIxOTc0MDA2fQ.AxHG99mbvujq8DGe1Yn-XNZivNbT7wCFd2br-X1UsAY"
{
  "detalhes": [
    {
      "chave": "exemplo1234567",
      "conteudo": {
        "descricao": "Exemplo de conte\u00fado",
        "pedido": "35463232"
      },
      "data": "Mon, 22 Jul 2024 00:00:00 GMT",
      "tipo": "marca",
      "usuario": "douglas"
    }
  ],
  "resultado": "ok"
}

$ curl -X POST localhost:5000/login -d "{\"login\":\"douglas@gmail.com\",\"senha\":\"douglas123\"}" -H "Content-Type: application/json" 
{
  "detalhes": "usuario ou senha incorreto(s)",
  "resultado": "erro"
}

$ curl localhost:5000/listar/Pessoa
{
  "msg": "Missing Authorization Header"
}

$ curl localhost:5000/listar/Consulta
{
  "msg": "Missing Authorization Header"
}

'''