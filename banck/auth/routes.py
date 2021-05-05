import bcrypt
from flask import Blueprint, request
from .schemas import login_schema
from banck.users.models import User
from banck.users.schemas import user_creation_schema
from banck.utils import create_error, generate_token


auth = Blueprint('auth', __name__)


@auth.route('/auth/login', methods=['POST'])
def login():
  if error := login_schema.validate(request.json):
    return create_error(error, 400)

  email = request.json.get('email')
  password = request.json.get('password')

  if user := User.query.filter_by(email=email).first():
    if bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8')):
      return { 'token': generate_token(user.id) }

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

  return { 'token': generate_token(user.id) }