from modelo.consulta import *
from geral.cripto import *
from modelo.usuario import *
# teste de consulta
def run():
    with db_session:
        user_id = Usuario.get(id=1)
        if user_id:
            print("usuario encontrado!")
            print("detalhes do usuario:")
            print(json.dumps(user_id.json(), indent=4))

            gerar_consulta = Consulta(tipo='marca', data=date.today(), chave='exemplo1234567', conteudo={'descricao': 'Exemplo de conteúdo', 'pedido': '35463232'}, usuario=user_id.json())
            print("consulta cadastrada com sucesso!")
            commit()
        else:
            print("usuario nao encontrado :(")

# OBS.: ainda será implementada uma automatização de todos os atributos 
# conforme as informações provenientes do webcrawler