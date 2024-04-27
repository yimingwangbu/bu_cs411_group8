from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_oauthlib.client import OAuth
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
oauth = OAuth()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config["SECRET_KEY"] = Config.SECRET_KEY

    db.init_app(app)
    login_manager.init_app(app)
    oauth.init_app(app)

    with app.app_context():
        db.create_all()  # Create database tables within the app context

    from app.routes import main
    app.register_blueprint(main)

    return app
