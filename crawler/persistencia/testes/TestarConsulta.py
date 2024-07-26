from modelo.consulta import *

# teste de consulta
def run():
    with db_session:
        diario = Consulta(usuario='douglas', tipo='marca', data=date(2024, 7, 22), chave='exemplo1234567', conteudo={'descricao': 'Exemplo de conteúdo', 'pedido': '35463232'})
        commit()
        print(diario.usuario, diario.tipo, diario.data, diario.id, diario.chave, diario.conteudo)

# OBS.: ainda será implementada uma automatização de todos os atributos 
# conforme as informações provenientes do webcrawler