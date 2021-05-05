import datetime, jwt
from flask import current_app


def create_error(message, status):
  return {
    'error': True,
    'message': message,
    'status': status
  }


def generate_token(user_id):
  payload = {
    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
    'iat': datetime.datetime.utcnow(),
    'sub': user_id,
  }

  return jwt.encode(
    payload,
    current_app.config.get('SECRET_KEY'),
    algorithm='HS256'
  )


def decode_token(token):
  return jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'])