from geral.config import *
from geral.cripto import *
from modelo.usuario import *

# rota para reset de senha
@app.route("/reinicializar_senha", methods=['POST'])

@jwt_required()
def reinicializar_senha():
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
            # identifica o usuario que terá sua senha resetada,
            # gera um token temporário (1 hora) utilizando a identidade do usuario e
            # criptografa a token para guarda-la no banco no lugar da senha original
            usuario = Usuario.get(email=identificacao)
            if usuario.id == 1:
              resposta = jsonify({"resultado":"erro","detalhes":"o usuario admin/root não pode ter seus dados alterados."})
            else:
              token = create_access_token(identity=usuario.email)
              usuario.senha = cifrar(token)
              commit()
              resposta = jsonify({"resultado":"ok","detalhes":token, "OBS.:": "(acesse sua conta utilizando a token contidas nos detalhes como senha e altere a senha em ate uma hora na rota /alterar_dados)"})
    else:
        resposta = jsonify({"resultado":"erro","detalhes":"atividade restrita ao usuario do tipo admin"})

  except Exception as e:
        resposta = jsonify({"resultado":"erro","detalhes":str(e)})
        print("ERRO: "+str(e))
  return resposta 

'''
RESULTADO DE TESTES:
curl -X POST localhost:5000/reinicializar_senha -d "{\"email\": \"juniorsales@gmail.com\"}" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMzE0MTY2MSwianRpIjoiMWE1NGViMzAtOTlmZS00MTYzLTkxMGQtODg3MTBhNTkzODcxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsInRpcG8iOiJhZG1pbiJ9LCJuYmYiOjE3MjMxNDE2NjEsImNzcmYiOiI1NmEzZjgxOS00ZWJjLTRkNzQtOTgxNC0wOTlhYjRlMDcxMzIiLCJleHAiOjE3MjMxNDUyNjF9.NsDalkE9SCZmTeukS-jP5JokuxDj3lNMMp4ObZV5ndM" -H "Content-Type: application/json"
{
  "OBS.:": "(acesse sua conta utilizando a token contidas nos detalhes como senha e altere a senha em ate uma hora na rota /alterar_dados)",
  "detalhes": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMzE0MzQwNCwianRpIjoiMDRkODU1YjEtYWE3NC00N2ZkLWI4ZjAtNWRlOWVkYzRmODY4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imp1bmlvcnNhbGVzQGdtYWlsLmNvbSIsIm5iZiI6MTcyMzE0MzQwNCwiY3NyZiI6IjkxMzcxNTRiLWNhN2ItNGM0OS1iODZmLWM4MWVjOWZlODYwYiIsImV4cCI6MTcyMzE0NzAwNH0.BkgWFXyZkUyTiHGzBj7qFVAP1fmMxtv68QUAGex2HSE",
  "resultado": "ok"
}'''