# importações
from flask import Flask, jsonify, request
# https://stackoverflow.com/questions/70383004/modulenotfounderror-no-module-named-flaskext

#importação do pony ORM
from pony.orm import *
from datetime import date
import json

from flask_cors import CORS

# configurações
app = Flask(__name__)

CORS(app)  

# importações de JWT
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from datetime import timedelta

app.config["JWT_SECRET_KEY"] = "super-secret" 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)
