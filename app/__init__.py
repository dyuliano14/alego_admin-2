from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin
from flask_wtf import CSRFProtect
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from config import Config
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
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