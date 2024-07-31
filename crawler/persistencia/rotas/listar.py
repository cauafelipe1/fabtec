from geral.config import *
from modelo.consulta import *
from modelo.usuario import *

#acessado pelo localhost:5000/listar/classe
@app.route("/listar/<string:classe>")
@jwt_required()

def listar(classe):    
    try:
        print("quem está acessando: ")
        current_user = get_jwt_identity()
        print(current_user)
        
        dados = None
        # lista os dados da tabela person.db
        if classe == "Usuario":
            with db_session:
                dados = Usuario.select()[:]
                print(dados)

        # lista os dados da tabela consult.db
        elif classe == "Consulta":
            with db_session:
                dados = Consulta.select()[:]
        
        # converção de dados para json
        lista_jsons = [x.json() for x in dados]
        # converção da lista do python para json
        resposta = jsonify({"resultado":"ok","detalhes":lista_jsons})

    except Exception as e:
        resposta = jsonify({"resultado":"erro","detalhes":str(e)})
        print("ERRO: "+str(e))
    return resposta