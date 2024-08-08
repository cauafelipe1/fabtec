from geral.config import *
from modelo.consulta import *
from modelo.usuario import *

# acessado pelo localhost:5000/listar/classe
@app.route("/listar/<string:classe>")
@jwt_required()

def listar(classe):    
    try:
        print("quem está acessando: ")
        current_user = get_jwt_identity()
        print(f"usuario: {current_user['email']}\ntipo: {current_user['tipo']}")
        if current_user['tipo'].lower() == "admin":
            with db_session:
                dados = None
                # lista os dados da tabela Usuario
                if classe == "Usuario":
                        dados = Usuario.select()[:]
                        

                # lista os dados da tabela Consulta
                elif classe == "Consulta":
                        dados = Consulta.select()[:]
                
                # conversão de dados para json
                lista_jsons = [x.json() for x in dados]

            # conversão da lista do python para json
            resposta = jsonify({"resultado":"ok","detalhes":lista_jsons})
        else:
            resposta = jsonify({"resultado":"erro","detalhes": "atividade restrita ao usuario admin"})
    except Exception as e:
        resposta = jsonify({"resultado":"erro","detalhes":str(e)})
        print("ERRO: "+str(e))
    return resposta

'''
RESULTADO DE TESTES:
curl localhost:5000/listar/Usuario -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMzEyOTI1MywianRpIjoiMGJiNmUzNzktNmQ4YS00OGFmLThkZGUtYzIxNWZmNTgxMTI5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsInRpcG8iOiJhZG1pbiJ9LCJuYmYiOjE3MjMxMjkyNTMsImNzcmYiOiJlMzM5MmE3MC03ODRmLTQ3NDAtODg5My1hZjRmNTU5ODE0MGUiLCJleHAiOjE3MjMxMzI4NTN9.GgoMpu7N8ay_DrO68Wmygt955RUIhi8XwWK5teejANQ"
{
  "detalhes": [
    {
      "cpf": "00000000000",
      "data de ativacao": "2024-08-08",
      "email": "admin@admin.com",
      "nome": "admin",
      "senha": "eba34065a1d45b3bfd700926b250ee119b42b331977b43b61f6c9d383fcb8f2d898d2b003253796e0eda3a37d3fdffd131758ad348e94dfe9685f787c7911a42",
      "tipo": "admin"
    },
    {
      "cpf": "123.456.789-09",
      "data de ativacao": "2024-08-08",
      "email": "charles@gmail.com",
      "nome": "charles",
      "senha": "b470687cef973be11788cc6fd294b306236ae2c57c7dc10099c8ddeb7c0d710e6ec95146ba3424dfea943714c263656bdc7b25d1dbbaa48611ccd808aaba6267",
      "tipo": "comum"
    }
  ],
  "resultado": "ok"
}
curl localhost:5000/listar/Consulta -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMzEyOTI1MywianRpIjoiMGJiNmUzNzktNmQ4YS00OGFmLThkZGUtYzIxNWZmNTgxMTI5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsInRpcG8iOiJhZG1pbiJ9LCJuYmYiOjE3MjMxMjkyNTMsImNzcmYiOiJlMzM5MmE3MC03ODRmLTQ3NDAtODg5My1hZjRmNTU5ODE0MGUiLCJleHAiOjE3MjMxMzI4NTN9.GgoMpu7N8ay_DrO68Wmygt955RUIhi8XwWK5teejANQ"
{
  "detalhes": [
    {
      "chave": "exemplo1234567",
      "conteudo": {
        "descricao": "Exemplo de conte\u00fado",
        "pedido": "35463232"
      },
      "data": "2024-08-08",
      "tipo": "marca",
      "usuario": {
        "cpf": "00000000000",
        "data de ativacao": "2024-08-08",
        "email": "admin@admin.com",
        "nome": "admin",
        "senha": "eba34065a1d45b3bfd700926b250ee119b42b331977b43b61f6c9d383fcb8f2d898d2b003253796e0eda3a37d3fdffd131758ad348e94dfe9685f787c7911a42",
        "tipo": "admin"
      }
    }
  ],
  "resultado": "ok"
}

$ curl localhost:5000/listar/Consulta -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMzEzMDI2MiwianRpIjoiOTg1ZjQ4MWQtMTdkMi00ODhmLWE4NzEtYmRkMTIwMDM3ZGIxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJlbWFpbCI6ImNoYXJsZXNAZ21haWwuY29tIiwidGlwbyI6ImNvbXVtIn0sIm5iZiI6MTcyMzEzMDI2MiwiY3NyZiI6IjI0OTg4YjhkLTdlZGQtNDk5NC05MDAwLTcwOTBkMmNiZjgwMiIsImV4cCI6MTcyMzEzMzg2Mn0.vb2R3B5SujebjsF03xKIPD6P4UPIgrWQSLzQBd2v50s"
{
  "detalhes": "atividade restrita ao usuario admin",
  "resultado": "erro"
}

$ curl localhost:5000/listar/Usuario -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMzEzMDI2MiwianRpIjoiOTg1ZjQ4MWQtMTdkMi00ODhmLWE4NzEtYmRkMTIwMDM3ZGIxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJlbWFpbCI6ImNoYXJsZXNAZ21haWwuY29tIiwidGlwbyI6ImNvbXVtIn0sIm5iZiI6MTcyMzEzMDI2MiwiY3NyZiI6IjI0OTg4YjhkLTdlZGQtNDk5NC05MDAwLTcwOTBkMmNiZjgwMiIsImV4cCI6MTcyMzEzMzg2Mn0.vb2R3B5SujebjsF03xKIPD6P4UPIgrWQSLzQBd2v50s"
{
  "detalhes": "atividade restrita ao usuario admin",
  "resultado": "erro"
}
$ curl localhost:5000/listar/Usuario
{
  "msg": "Missing Authorization Header"
}

$ curl localhost:5000/listar/Consulta
{
  "msg": "Missing Authorization Header"
}'''