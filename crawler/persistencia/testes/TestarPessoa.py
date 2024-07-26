from modelo.pessoa import *
from geral.cripto import *

# testes da classe pessoa
def run():
    with db_session:
        p1 = Pessoa(nome='douglas', cpf='12345678901', email='douglas@gmail.com', senha= cifrar('12345678'))
        p2 = Pessoa(nome='hugo', cpf='11111111111', email='hugo@gmail.com', senha= cifrar('hugo123'))
        commit()