from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin
from flask_wtf import CSRFProtect
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from config import Config
from flask_cors import CORS
import os
import logging
from logging.handlers import RotatingFileHandler


db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'main.login_view' # Corrigido para corresponder à função login_view
login_manager.login_message_category = 'info' # Opcional: para estilizar a mensagem de "login necessário"
jwt = JWTManager()




def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['JWT_SECRET_KEY'] = 'dyu1412'
    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)  # ✅ Inicializa o Migrate corretamente
    csrf.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)
    if not app.debug:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/alego_admin.log', maxBytes=10240, backupCount=5)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s [%(levelname)s] - %(message)s [em %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

            app.logger.setLevel(logging.INFO)
            app.logger.info('Alego Admin Iniciado')
                     
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes import main
    app.register_blueprint(main)

    from .api import api
    app.register_blueprint(api)
    csrf.exempt(api)
       
    return app