from geral.config import *
from geral.cripto import *
from modelo.usuario import *

# rota para cadastrar novos usuarios
@app.route("/cadastrar", methods=['POST'])
def cadastrar():
    
  with db_session:
    # recebe os dados do curl
    dados = request.get_json()
    login = dados['email']
    senha = dados['senha']

    # verfica se os dados fornecidos no curl já não estão presentes no banco
    encontrado = Usuario.get(email=login, senha=cifrar(senha))
    
    # caso nao seja encontrado, valida o cpf e cadastra os dados
    if encontrado is None: 
        if validador_cpf(dados['cpf']):
            novo_usuario = Usuario(tipo="comum", nome=dados['nome'], cpf=dados['cpf'], email=dados['email'], senha= cifrar(dados['senha']), data_ativacao= date.today(), situacao="ativo")
            commit()
            resposta = jsonify({"resultado": "ok", "detalhes":"novo usuario adicionado!"})
        else:
           resposta = jsonify({"resultado": "erro", "detalhes": "CPF invalido."})

    else:        
        resposta = jsonify({"resultado": "usuario identificado", "detalhes": "os dados ja estao crendenciados em nosso banco"}) 
 
  return resposta 
'''
RESULTADO DE TESTES:

$ curl -X POST localhost:5000/cadastrar -d "{\"nome\": \"charles\", \"cpf\": \"123.456.789-09\", \"email\": \"charles@gmail.com\", \"senha\": \"charles123\"}" -H "Content-Type: application/json"
{
  "detalhes": "novo usuario adicionado!",
  "resultado": "ok"
}

$ curl -X POST localhost:5000/cadastrar -d "{\"nome\": \"charles\", \"cpf\": \"123.456.789-09\", \"email\": \"charles@gmail.com\", \"senha\": \"charles123\"}" -H "Content-Type: application/json"
{
  "detalhes": "os dados ja estao crendenciados em nosso banco",
  "resultado": "usuario identificado"
}'''