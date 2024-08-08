from geral.config import *



# criação da classe Usuario (usuário que fará o login)
class Usuario(db.Entity):
    tipo = Required(str)
    nome = Required(str)
    cpf = Required(str)
    email = Required(str)
    senha = Required(str)
    data_ativacao = Optional(date, nullable=True)
    consultas = Set('Consulta')
    # relacao um para muitos entre usuarios e consultas
    
    # expressão da classe em str
    def __str__(self):
        return f'{str(self.tipo)}, {self.nome}, {str(self.cpf)}, ' +\
               f'{self.email}, {self.senha}, {str(self.data_ativacao)}'

    # expressao da classe no formato json
    def json(self):
        return {
            "tipo": self.tipo,
            "nome": self.nome,
            "cpf": self.cpf,
            "email": self.email,
            "senha": self.senha,
            "data de ativacao": str(self.data_ativacao),
        }


# validador de cpf
def validador_cpf(cpf_usado: str) -> bool:
    # remove os valores não numerico do cpf
    cpf_usado = ''.join(filter(str.isdigit, cpf_usado))

     # verifica se o cpf tem 11 dígitos e se não é uma sequência repetida
    if len(cpf_usado) != 11 or cpf_usado == cpf_usado[0] * 11:
        return False
    
     # calculo do primeiro dígito verificador
    sum1 = sum(int(cpf_usado[i]) * (10 - i) for i in range(9))
    check1 = (sum1 * 10 % 11) % 10

    # calculo do segundo dígito verificador
    sum2 = sum(int(cpf_usado[i]) * (11 - i) for i in range(10))
    check2 = (sum2 * 10 % 11) % 10

     # verifica se os digitos verificadores estão corretos
    return check1 == int(cpf_usado[9]) and check2 == int(cpf_usado[10])

# OBS.: Nome de variável alterado para cpf_usado para não haver conflito com o atributo cpf
# OBS.2: o validador ainda não verifica se o cpf é de fato do usuario que incluiu seus dados
