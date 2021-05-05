import jwt
from functools import wraps
from flask import request
from banck.users.models import User
from banck.utils import create_error, decode_token


def is_authenticated(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    try:
      user_id = kwargs.get('user_id')
      if user := User.query.filter_by(id=user_id).first():
        decoded_user = decode_token(request.args.get('token'))
        if user.id == user_id or decoded_user.get('admin'):
          return func(*args, **kwargs)

        return create_error('Invalid token. Please log in again!', 400)
      return create_error('User not found!', 404)
    except jwt.ExpiredSignatureError:
      return create_error('Signature expired. Please log in again.', 401)
    except jwt.InvalidTokenError:
      return create_error('Invalid token. Please log in again.', 400)

  return wrapper


def is_authorized(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    try:
      if decode_token(request.args.get('token')).get('admin'):
        return func(*args, **kwargs)

      return create_error('User is not authorized!', 401)
    except jwt.ExpiredSignatureError:
      return create_error('Signature expired. Please log in again.', 401)
    except jwt.InvalidTokenError:
      return create_error('Invalid token. Please log in again.', 400)

  return wrapper