from geral.config import *
from geral.cripto import *
from modelo.usuario import *

# rota para alteração de dados
# ficou meio bagunçada mas acho que dá para entender
@app.route("/alterar_dados", methods=['POST'])

@jwt_required()
def alterar_dados():
  try: 
    # identificação de usuario
    print("quem está acessando: ")
    current_user = get_jwt_identity()
    # variaveis que pegam o email e o tipo do usuario que utilizou o token (JWT)
    user_email = current_user['email']
    user_type = current_user['tipo']
    print(f"usuario: {user_email}\ntipo: {user_type}")

    # requisição dos dados fornecidos no curl
    dados = request.get_json()

    with db_session:
        
        # função que atualiza os dados
        def atualizar_dados(usuario):

            # validação do cpf
            if validador_cpf(dados['cpf']):

                # cpf valido = dados aptos para serem alterados 
                usuario.nome = dados['nome']
                usuario.email = dados['email']
                usuario.senha = cifrar(dados['senha'])
                usuario.cpf = dados['cpf']

                # caso o usuario seja admin, poderá alterar o grau de hierarquia do usuario
                if user_type.lower() == "admin":
                    usuario.tipo = dados['tipo'].lower()
                commit()
                resposta = jsonify({"resultado":"ok","detalhes":f"os dados do usuario foram alterados com sucesso!"})
            else:
                resposta = jsonify({"resultado":"erro","detalhes":f"CPF inválido"})
            return resposta
        
        # caso o usuario seja comum, solicita a alteração dos proprios dados
        if user_type.lower() != "admin":
            usuario = Usuario.get(email=user_email)
            print(usuario)
            resposta = atualizar_dados(usuario)

        # caso contrário (admin), recebe o id fornecido pelo curl e altera os dados
        else:
            usuario = Usuario[int(dados['id'])]

            # nem mesmo usuarios admin poderão alterar os valores do admin de id 1 (root)
            if usuario.id == 1:
                resposta = jsonify({"resultado":"erro","detalhes":f"os dados do usuario admin/root nao podem ser alterados"})
            
            # talvez pareça meio confuso, mas este elif verifica a existência do usuário
            elif usuario:
                print(usuario)
                resposta = atualizar_dados(usuario)
            else:
                resposta = jsonify({"resultado":"erro","detalhes":f"usuario não encontrado"})
                
          
  except Exception as e:
        resposta = jsonify({"resultado":"erro","detalhes":str(e)})
        print("ERRO: "+str(e))
  return resposta 