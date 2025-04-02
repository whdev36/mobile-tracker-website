# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_socketio import SocketIO

import dotenv
import os
dotenv.load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mt.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)
socketio = SocketIO(app, cors_allowed_origins='*')

login_manager.login_view = 'login'
login_manager.login_message = 'Ushbu sahifaga kirish uchun avval tizimga kiring.'
login_manager.login_message_category = 'info'

from app import routes