from geral.config import *
db = Database()

# criação da classe Pessoa (usuário que fará o login)
class Pessoa(db.Entity):
    nome = Required(str)
    cpf = Required(str)
    email = Required(str)
    senha = Required(str)
    
    # expressão da classe em str
    def __str__(self):
        return f'{self.nome} [cpf={str(self.cpf)}], ' +\
               f'{self.email}, {self.senha}'

    # expressao da classe no formato json
    def json(self):
        return {
            "nome": self.nome,
            "cpf": self.cpf,
            "email": self.email,
            "senha": self.senha
        }

#criação do banco de dados sqlites
db.bind(provider='sqlite', filename='person.db', create_db=True)
db.generate_mapping(create_tables=True)
