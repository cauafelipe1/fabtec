from geral.config import *
from geral.cripto import *
from modelo.usuario import *

# rota para alteração de dados
# ficou meio bagunçada mas acho que dá para entender
@app.route("/controlar_situacao/<string:situacao>", methods=['POST'])

@jwt_required()
def controlar_situacao(situacao):
  try: 
    # identificação de usuario
    print("quem está acessando: ")
    current_user = get_jwt_identity()
    # variaveis que pegam o email e o tipo do usuario que utilizou o token (JWT)
    user_email = current_user['email']
    user_type = current_user['tipo']
    print(f"usuario: {user_email}\ntipo: {user_type}")

    # verifica se está sendo acessada por um admin
    if user_type == "admin":
        # requisição dos dados fornecidos no curl
        dados = request.get_json()
        identificacao = dados['email']
        
        with db_session:
            usuario = Usuario.get(email=identificacao)
            if usuario.id == 1:  
              resposta = jsonify({"resultado":"erro","detalhes":"usuario admin/root não pode ser desativado"})
            else:
              if situacao == "ativar":      
                  usuario.data_ativacao = date.today()
                  commit()
                  resposta = jsonify({"resultado":"ok","detalhes":"usuario ativado com sucesso!"})
              if situacao == "desativar":
                  usuario.data_ativacao = None
                  commit()
                  resposta = jsonify({"resultado":"ok","detalhes":"usuario desativado com sucesso!"})

    else:
        resposta = jsonify({"resultado":"erro","detalhes":"atividade restrita ao usuario do tipo admin"})

  except Exception as e:
        resposta = jsonify({"resultado":"erro","detalhes":str(e)})
        print("ERRO: "+str(e))
  return resposta 

''' 
RESULTADOS DE TESTES:

$ curl -X POST localhost:5000/controlar_situacao/desativar -d "{\"email\": \"juniorsales@gmail.com\"}" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMzE0MTY2MSwianRpIjoiMWE1NGViMzAtOTlmZS00MTYzLTkxMGQtODg3MTBhNTkzODcxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsInRpcG8iOiJhZG1pbiJ9LCJuYmYiOjE3MjMxNDE2NjEsImNzcmYiOiI1NmEzZjgxOS00ZWJjLTRkNzQtOTgxNC0wOTlhYjRlMDcxMzIiLCJleHAiOjE3MjMxNDUyNjF9.NsDalkE9SCZmTeukS-jP5JokuxDj3lNMMp4ObZV5ndM" -H "Content-Type: application/json"
{
  "detalhes": "usuario desativado com sucesso!",
  "resultado": "ok"
}

$ curl -X POST localhost:5000/controlar_situacao/ativar -d "{\"email\": \"juniorsales@gmail.com\"}" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMzE0MTY2MSwianRpIjoiMWE1NGViMzAtOTlmZS00MTYzLTkxMGQtODg3MTBhNTkzODcxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsInRpcG8iOiJhZG1pbiJ9LCJuYmYiOjE3MjMxNDE2NjEsImNzcmYiOiI1NmEzZjgxOS00ZWJjLTRkNzQtOTgxNC0wOTlhYjRlMDcxMzIiLCJleHAiOjE3MjMxNDUyNjF9.NsDalkE9SCZmTeukS-jP5JokuxDj3lNMMp4ObZV5ndM" -H "Content-Type: application/json"
{
  "detalhes": "usuario ativado com sucesso!",
  "resultado": "ok"
}


'''