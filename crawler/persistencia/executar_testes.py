from modelo.consulta import *
from modelo.usuario import *
from testes import *

with app.app_context():
    TestarCifrar.run()
    TestarCriarAdmin.run()
    TestarConsulta.run()