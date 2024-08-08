from modelo.consulta import *
from modelo.usuario import *
from geral.cripto import *

# teste de consulta
def run():
    # uma base da ideia principal quando a rota consultar for criada
    with db_session:
        # aqui será encontrado o usuario que está fazendo a requisição
        user = Usuario.get(id=1)
        if user:
            print("usuario encontrado!")
            print("detalhes do usuario:")
            print(json.dumps(user.json(), indent=4))

            # haverá uma verificação se a consulta já está cadastrada. Exemplo em pseudo-python:
            # dados = request.get_json()
            # if Consulta.exists(tipo= dados['tipo'], chave= dados['chave']):
            #   retorna o conteudo da consulta já registrada no banco de dados
            # else:
            #   utiliza o crowler
            #   cadastra no banco (esse trambolho todo ai debaixo)
            #   retorna o conteudo

            gerar_consulta = Consulta(tipo='marca', data=date.today(), chave='exemplo1234567', conteudo={'descricao': 'Exemplo de conteúdo', 'pedido': '35463232'}, usuario=user)
            commit()
            print("consulta cadastrada com sucesso!")
            print("detalhes da consulta:")
            x = Consulta.get(tipo='marca', chave='exemplo1234567')
            print(json.dumps(x.json(), indent=4))
        else:
            print("usuario nao encontrado :(")

# OBS.: ainda será implementada uma automatização de todos os atributos 
# conforme as informações provenientes do webcrawler