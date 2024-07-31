from modelo.usuario import *
from geral.cripto import *

# testes da classe pessoa
def run():
    with db_session:
        admin = Usuario(nome="admin", cpf="00000000000", email="admin@admin.com", senha= cifrar("admin123"), data_cadastro= date.today(), situacao="ativo")
        print("usuario admin criado com sucesso!")
        commit()