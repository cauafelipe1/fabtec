from geral.config import *
from modelo.consulta import *
from modelo.usuario import *
from rotas import *
from geral.cripto import *
# programa responsável por rodar o sistema
with app.app_context():

    @app.route("/")
    def inicio():
        return 'o sistema está em funcionamento!'
    app.run(debug=True, host="0.0.0.0")