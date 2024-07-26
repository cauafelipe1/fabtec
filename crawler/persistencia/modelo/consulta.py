from geral.config import *


db = Database()

# criação da classe consulta
class Consulta(db.Entity):
    usuario = Required(str)
    tipo = Required(str)
    data = Required(date)
    chave = Required(str)
    conteudo = Required(Json)

    # expressão da classe no formato str
    def __str__(self):
        return f'{self.usuario} {str(self.tipo)}, ' +\
               f'{self.data}, {self.chave}, {self.conteudo}'

    # expressao da classe no formato json
    def json(self):
        return {
            "usuario": self.usuario,
            "tipo": self.tipo,
            "data": self.data,
            "chave": self.chave,
            "conteudo": self.conteudo,
        }
# criação do banco de dados sqlite
db.bind(provider='sqlite', filename='consult.db', create_db=True)
db.generate_mapping(create_tables=True)

