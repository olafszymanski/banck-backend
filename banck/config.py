import os
from dotenv import load_dotenv


load_dotenv()


class Config:
  DEBUG = False
  SECRET_KEY = os.environ.get('SECRET_KEY')
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
  SQLALCHEMY_TRACK_MODIFICATIONS = False


class DebugConfig(Config):
  DEBUG = True