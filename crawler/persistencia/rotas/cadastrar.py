from geral.config import *
from geral.cripto import *
from modelo.usuario import *

# rota para cadastrar novos usuarios
@app.route("/cadastrar", methods=['POST'])

@jwt_required()
def cadastrar():
  try: 
    print("quem está acessando: ")
    current_user = get_jwt_identity()
    user_email = current_user['email']
    user_type = current_user['tipo']
    print(f"usuario: {user_email}\ntipo: {user_type}")

    
    if user_type.lower() != "admin":
      resposta = jsonify({"resultado":"erro","detalhes": "atividade restrita ao usuario do tipo admin"})
    
    else:
      with db_session:
        # recebe os dados do curl
        dados = request.get_json()
        login = dados['email']

        # verfica se o dado chave (email) fornecido no curl já está presente no banco
        encontrado = Usuario.get(email=login) #restrição ao email para não haver o caso do mesmo email com várias senhas diferentes
        
        # caso nao seja encontrado, valida o cpf, o tipo do usuario e cadastra os dados
        if encontrado is None: 
            
            # validação do cpf
            if validador_cpf(dados['cpf']):
                
                # verificação do tipo de usuário
                if (dados['tipo'].lower() == "comum") or  (dados['tipo'].lower() == "admin"):
                  novo_usuario = Usuario(tipo=dados['tipo'].lower(), nome=dados['nome'], cpf=dados['cpf'], email=dados['email'], senha= cifrar(dados['senha']), data_ativacao= date.today())
                  commit()
                  resposta = jsonify({"resultado": "ok", "detalhes":"novo usuario adicionado!"})
                else:
                  resposta = jsonify({"resultado": "erro", "detalhes": "tipo de usuario inválido"})

            else:
              resposta = jsonify({"resultado": "erro", "detalhes": "CPF invalido."})

        else:        
            resposta = jsonify({"resultado": "usuario identificado", "detalhes": "os dados inseridos ja estao crendenciados no banco"}) 
    
  except Exception as e:
        resposta = jsonify({"resultado":"erro","detalhes":str(e)})
        print("ERRO: "+str(e))
  return resposta 
  
'''
RESULTADO DE TESTES:

$ curl -X POST localhost:5000/cadastrar -d "{\"tipo\": \"comum\", \"nome\": \"charles\", \"cpf\": \"123.456.789-09\", \"email\": \"charles@gmail.com\", \"senha\": \"charles123\"}" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMzEyOTI1MywianRpIjoiMGJiNmUzNzktNmQ4YS00OGFmLThkZGUtYzIxNWZmNTgxMTI5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsInRpcG8iOiJhZG1pbiJ9LCJuYmYiOjE3MjMxMjkyNTMsImNzcmYiOiJlMzM5MmE3MC03ODRmLTQ3NDAtODg5My1hZjRmNTU5ODE0MGUiLCJleHAiOjE3MjMxMzI4NTN9.GgoMpu7N8ay_DrO68Wmygt955RUIhi8XwWK5teejANQ" -H "Content-Type: application/json"
{
  "detalhes": "novo usuario adicionado!",
  "resultado": "ok"
}

$ curl -X POST localhost:5000/cadastrar -d "{\"tipo\": \"comum\", \"nome\": \"charles\", \"cpf\": \"123.456.789-09\", \"email\": \"charles@gmail.com\", \"senha\": \"charles123\"}" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMzEyOTI1MywianRpIjoiMGJiNmUzNzktNmQ4YS00OGFmLThkZGUtYzIxNWZmNTgxMTI5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsInRpcG8iOiJhZG1pbiJ9LCJuYmYiOjE3MjMxMjkyNTMsImNzcmYiOiJlMzM5MmE3MC03ODRmLTQ3NDAtODg5My1hZjRmNTU5ODE0MGUiLCJleHAiOjE3MjMxMzI4NTN9.GgoMpu7N8ay_DrO68Wmygt955RUIhi8XwWK5teejANQ" -H "Content-Type: application/json"
{
  "detalhes": "os dados inseridos ja estao crendenciados no banco",
  "resultado": "usuario identificado"
}

** testes usando usuario admin e comum **
token do admin: {eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMzEyOTI1MywianRpIjoiMGJiNmUzNzktNmQ4YS00OGFmLThkZGUtYzIxNWZmNTgxMTI5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsInRpcG8iOiJhZG1pbiJ9LCJuYmYiOjE3MjMxMjkyNTMsImNzcmYiOiJlMzM5MmE3MC03ODRmLTQ3NDAtODg5My1hZjRmNTU5ODE0MGUiLCJleHAiOjE3MjMxMzI4NTN9.GgoMpu7N8ay_DrO68Wmygt955RUIhi8XwWK5teejANQ}
token do usuario comum: {eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMzEzMDI2MiwianRpIjoiOTg1ZjQ4MWQtMTdkMi00ODhmLWE4NzEtYmRkMTIwMDM3ZGIxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJlbWFpbCI6ImNoYXJsZXNAZ21haWwuY29tIiwidGlwbyI6ImNvbXVtIn0sIm5iZiI6MTcyMzEzMDI2MiwiY3NyZiI6IjI0OTg4YjhkLTdlZGQtNDk5NC05MDAwLTcwOTBkMmNiZjgwMiIsImV4cCI6MTcyMzEzMzg2Mn0.vb2R3B5SujebjsF03xKIPD6P4UPIgrWQSLzQBd2v50s}

# cadastrado utilizando o token do admin

$ curl -X POST localhost:5000/cadastrar -d "{\"tipo\": \"Admin\", \"nome\": \"junior\", \"cpf\": \"987.654.321-00\", \"email\": \"junior@gmail.com\", \"senha\": \"junior123\"}" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMzEyOTI1MywianRpIjoiMGJiNmUzNzktNmQ4YS00OGFmLThkZGUtYzIxNWZmNTgxMTI5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsInRpcG8iOiJhZG1pbiJ9LCJuYmYiOjE3MjMxMjkyNTMsImNzcmYiOiJlMzM5MmE3MC03ODRmLTQ3NDAtODg5My1hZjRmNTU5ODE0MGUiLCJleHAiOjE3MjMxMzI4NTN9.GgoMpu7N8ay_DrO68Wmygt955RUIhi8XwWK5teejANQ" -H "Content-Type: application/json"
{
  "detalhes": "novo usuario adicionado!",
  "resultado": "ok"
}

# tentativa de cadastro usando o token do usuario comum
$ curl -X POST localhost:5000/cadastrar -d "{\"tipo\": \"comum\", \"nome\": \"belchior\", \"cpf\": \"012.345.678-90\", \"email\": \"belchior@gmail.com\", \"senha\": \"belchior123\"}" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMzEzMDI2MiwianRpIjoiOTg1ZjQ4MWQtMTdkMi00ODhmLWE4NzEtYmRkMTIwMDM3ZGIxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJlbWFpbCI6ImNoYXJsZXNAZ21haWwuY29tIiwidGlwbyI6ImNvbXVtIn0sIm5iZiI6MTcyMzEzMDI2MiwiY3NyZiI6IjI0OTg4YjhkLTdlZGQtNDk5NC05MDAwLTcwOTBkMmNiZjgwMiIsImV4cCI6MTcyMzEzMzg2Mn0.vb2R3B5SujebjsF03xKIPD6P4UPIgrWQSLzQBd2v50s" -H "Content-Type: application/json"
{
  "detalhes": "atividade restrita ao usuario do tipo admin",
  "resultado": "erro"
}

# agora com o token do admin
$ curl -X POST localhost:5000/cadastrar -d "{\"tipo\": \"comum\", \"nome\": \"belchior\", \"cpf\": \"012.345.678-90\", \"email\": \"belchior@gmail.com\", \"senha\": \"belchior123\"}" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMzEyOTI1MywianRpIjoiMGJiNmUzNzktNmQ4YS00OGFmLThkZGUtYzIxNWZmNTgxMTI5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsInRpcG8iOiJhZG1pbiJ9LCJuYmYiOjE3MjMxMjkyNTMsImNzcmYiOiJlMzM5MmE3MC03ODRmLTQ3NDAtODg5My1hZjRmNTU5ODE0MGUiLCJleHAiOjE3MjMxMzI4NTN9.GgoMpu7N8ay_DrO68Wmygt955RUIhi8XwWK5teejANQ" -H "Content-Type: application/json"
{
  "detalhes": "novo usuario adicionado!",
  "resultado": "ok"
}

#usuario ja cadastrado
$ curl -X POST localhost:5000/cadastrar -d "{\"tipo\": \"comum\", \"nome\": \"belchior\", \"cpf\": \"012.345.678-90\", \"email\": \"belchior@gmail.com\", \"senha\": \"belchior123\"}" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMzEyOTI1MywianRpIjoiMGJiNmUzNzktNmQ4YS00OGFmLThkZGUtYzIxNWZmNTgxMTI5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsInRpcG8iOiJhZG1pbiJ9LCJuYmYiOjE3MjMxMjkyNTMsImNzcmYiOiJlMzM5MmE3MC03ODRmLTQ3NDAtODg5My1hZjRmNTU5ODE0MGUiLCJleHAiOjE3MjMxMzI4NTN9.GgoMpu7N8ay_DrO68Wmygt955RUIhi8XwWK5teejANQ" -H "Content-Type: application/json"
{
  "detalhes": "os dados inseridos ja estao crendenciados no banco",
  "resultado": "usuario identificado"
}'''