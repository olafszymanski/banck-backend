from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from .config import DebugConfig


db = SQLAlchemy()
ma = Marshmallow()


def create_app(config_object=DebugConfig):
  app = Flask(__name__)
  app.config.from_object(config_object)

  from .users.routes import users
  from .auth.routes import auth

  app.register_blueprint(users)
  app.register_blueprint(auth)

  db.init_app(app)
  ma.init_app(app)

  return app