from modelo.consulta import *
from geral.cripto import *
from modelo.usuario import *
# teste de consulta
def run():
    # uma base da ideia principal quando a rota consultar for criada
    with db_session:
        # aqui será encontrado o usuario que está fazendo a requisição
        user_id = Usuario.get(id=1)
        if user_id:
            print("usuario encontrado!")
            print("detalhes do usuario:")
            print(json.dumps(user_id.json(), indent=4))

            # haverá uma verificação se a consulta já está cadastrada. Exemplo em pseudo-python:
            # dados = request.get_json()
            # verificar_consulta = Consulta.get(tipo= dados['tipo'], chave= dados['chave'])
            # if verificar_consulta is not None:
            #   retorna o conteudo da consulta já registrada no banco de dados
            # else:
            #   utiliza o crowler
            #   cadastra no banco (esse trambolho todo ai debaixo)
            #   retorna o conteudo

            gerar_consulta = Consulta(tipo='marca', data=date.today(), chave='exemplo1234567', conteudo={'descricao': 'Exemplo de conteúdo', 'pedido': '35463232'}, usuario=user_id.json())
            print("consulta cadastrada com sucesso!")
            commit()
        else:
            print("usuario nao encontrado :(")

# OBS.: ainda será implementada uma automatização de todos os atributos 
# conforme as informações provenientes do webcrawler