from modelo.usuario import *
from geral.cripto import *

# testes da criação de um usuario admin
def run():
    with db_session:
        if Usuario.exists(id=1):
            print("O admin/root já está operante!")
        else:
            admin = Usuario(tipo="admin", nome="admin", cpf="00000000000", email="admin@admin.com", senha= cifrar("admin123"), data_ativacao= date.today())
            print("usuario admin criado com sucesso!")
            commit()

# OBS.: Já está sendo criado automaticamente no arquivo consulta.py
