import bcrypt, jwt
from flask import Blueprint, request, current_app
from .schemas import login_schema
from banck.users.models import User
from banck.users.schemas import user_creation_schema
from banck.utils import create_error, generate_token, generate_refresh_token, decode_token


auth = Blueprint('auth', __name__)


@auth.route('/auth/login', methods=['POST'])
def login():
  if error := login_schema.validate(request.json):
    return create_error(error, 400)

  email = request.json.get('email')
  password = request.json.get('password')

  if user := User.query.filter_by(email=email).first():
    print(password.encode('utf8'))
    print(user.password.encode('utf8'))
    if bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8')):
      return {
        'token': generate_token(user),
        'refresh_token': generate_refresh_token(user)
      }

    return create_error('Incorrect password!', 403)

  return create_error('User not found!', 404)


@auth.route('/auth/signup', methods=['POST'])
def signup():
  if error := user_creation_schema.validate(request.json):
    return create_error(error, 400)

  user = User(
    request.json.get('name'),
    request.json.get('last_name'),
    request.json.get('email'),
    bcrypt.hashpw(request.json.get('password').encode('utf8'), bcrypt.gensalt())
  )
  if user.exists():
    return create_error('User already exists!', 409)

  user.add()

  return {
    'token': generate_token(user),
    'refresh_token': generate_refresh_token(user)
  }


@auth.route('/auth/refresh_token', methods=['GET'])
def refresh_token():
  if token := request.args.get('token'):
    try:
      decoded_token = decode_token(token)
      user_id = decoded_token.get('id')
      if user := User.query.filter_by(id=user_id).first():
        decoded_key = decoded_token.get('key')
        current_key = current_app.config.get('SECRET_KEY') + user.password
        if bcrypt.checkpw(current_key.encode('utf8'), decoded_key.encode('utf8')):
          return { 'token': generate_token(user) }

        return create_error('Password changed!', 401)
      return create_error('User not found!', 404)
    except jwt.ExpiredSignatureError:
      return create_error('Signature expired. Please log in again.', 401)
    except jwt.InvalidTokenError:
      return create_error('Invalid token. Please log in again.', 400)

  return create_error('No refresh token specified!', 404)