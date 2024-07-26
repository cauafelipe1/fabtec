from geral.config import *
from modelo.consulta import *
from rotas import *

#programa responsável por rodar o sistema
with app.app_context():

    @app.route("/")
    def inicio():
        return 'backend operante, operação de editar'

    app.run(debug=True, host="0.0.0.0")