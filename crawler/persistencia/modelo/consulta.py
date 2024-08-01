from geral.config import *
from modelo.usuario import Usuario, db

# criação da classe consulta
class Consulta(db.Entity):
    tipo = Required(str)
    data = Required(date)
    chave = Required(str)
    conteudo = Required(Json)
    usuario = Required(Usuario)

    # expressão da classe no formato str
    def __str__(self):
        return f'{str(self.tipo)}, {self.data}' +\
               f'{self.chave}, {self.conteudo}' +\
               f'{self.usuario}'

    # expressão da classe no formato json
    def json(self):
        return {
            "tipo": self.tipo,
            "data": str(self.data),
            "chave": self.chave,
            "conteudo": self.conteudo,
            "usuario": self.usuario.json(),
        }

# criação do banco de dados sqlite
db.bind(provider='sqlite', filename='consultas.db', create_db=True)
db.generate_mapping(create_tables=True)

