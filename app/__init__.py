import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from app.config import TestingConfig, Config

db = SQLAlchemy()
migrate = Migrate()

login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(testing=False):
    app = Flask(__name__)
    flask_env = os.getenv("FLASK_ENV", "production")  # Если переменной нет, по умолчанию ставим production

    if testing or flask_env == "testing":
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app.routes.auth_routes import auth_bp
    from app.routes.user_routes import user_bp
    from app.routes.user_routes import base_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(base_bp)

    login_manager.login_view = 'auth.login'

    from app.models.user import User
    from app.models.role import Role
    print("Текущая БД:", app.config['SQLALCHEMY_DATABASE_URI'])

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # with app.app_context():
    #     users = User.query.all()
    #     print("📋 Пользователи в базе:")
    #     for user in users:
    #         print(f"ID: {user.id}, Username: {user.username}, pass: {user.password_hash}")
    # with app.app_context():
    #     print("📋 Роли в базе:")
    #     for role in Role.query.all():
    #         print(f"ID: {role.id}, Name: {role.name}, pass: {role.description}")

    return app