from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object('config')

login_manager = LoginManager(app)

bcrypt = Bcrypt(app)

db = SQLAlchemy(app)