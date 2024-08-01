from modelo.usuario import *
from geral.cripto import *

# testes da criação de um usuario admin
def run():
    with db_session:
        admin = Usuario(tipo="admin", nome="admin", cpf="00000000000", email="admin@admin.com", senha= cifrar("admin123"), data_ativacao= date.today(), situacao="ativo")
        print("usuario admin criado com sucesso!")
        commit()