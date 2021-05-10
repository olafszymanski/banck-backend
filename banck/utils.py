import datetime, jwt, bcrypt
from flask import current_app


def create_error(message, status):
  return {
    'error': True,
    'message': message,
    'status': status
  }


def generate_key(password):
  key = current_app.config.get('SECRET_KEY') + password
  return bcrypt.hashpw(key.encode('utf8'), bcrypt.gensalt()).decode('utf8')


def generate_token(user):
  payload = {
    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
    'iat': datetime.datetime.utcnow(),
    'id': user.id,
    'admin': user.admin
  }

  return jwt.encode(
    payload,
    current_app.config.get('SECRET_KEY'),
    algorithm='HS256'
  )


def generate_refresh_token(user):
  payload = {
    'iat': datetime.datetime.utcnow(),
    'id': user.id,
    'key': generate_key(user.password)
  }

  return jwt.encode(
    payload,
    current_app.config.get('SECRET_KEY'),
    algorithm='HS256'
  )


def decode_token(token):
  return jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'])