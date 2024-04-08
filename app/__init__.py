import os
from flask import Flask
from config import config_by_name
from app.extensions.db import engine
from app.models import Base
from app.auth import bp_auth
from flask_login import LoginManager


login_manager = LoginManager()


def create_app(config_name):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True,
                subdomain_matching=True)
    app.config.from_object(config_by_name[config_name])

    Base.metadata.create_all(bind=engine)  # create all DB tables
    login_manager.init_app(app=app, add_context_processor=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(bp_auth, url_prefix='/auth')

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
