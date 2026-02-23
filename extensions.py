"""
Inițializarea extensiilor Flask.
Importate separat pentru a evita importurile circulare.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_babel import Babel

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
babel = Babel()

# Configurare login manager
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'
login_manager.login_message = 'Te rugăm să te autentifici pentru a accesa această pagină.'
