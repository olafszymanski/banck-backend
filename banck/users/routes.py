import bcrypt
from flask import Blueprint, jsonify, request
from .models import User
from .schemas import user_schema, users_schema, user_creation_schema
from banck.auth.decorators import is_authenticated, is_authorized
from banck.utils import create_error


users = Blueprint('users', __name__)


@users.route('/api/users/<int:user_id>', methods=['GET'])
@is_authenticated
def get_user(user_id):
  if user := User.query.filter_by(id=user_id).first():
    return user_schema.dump(user)

  return create_error('User not found!', 404)


@users.route('/api/users', methods=['GET'])
@is_authorized
def get_users():
  return jsonify(users_schema.dump(User.query.all()))


@users.route('/api/users', methods=['POST'])
def create_user():
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

  return user_schema.dump(user)


@users.route('/api/users/<int:user_id>', methods=['PUT'])
@is_authenticated
def update_user(user_id):
  if user := User.query.filter_by(id=user_id).first():
    if 'name' in request.json:
      user.name = request.json.get('name')
    if 'last_name' in request.json:
      user.last_name = request.json.get('last_name')
    if 'email' in request.json:
      user.email = request.json.get('email')
    if 'password' in request.json:
      user.password = bcrypt.hashpw(request.json.get('password').encode('utf8'), bcrypt.gensalt())
    if 'balance' in request.json:
      user.balance = request.json.get('balance')

    return user_schema.dump(user.update())

  return create_error('User not found!', 404)


@users.route('/api/users/<int:user_id>', methods=['DELETE'])
@is_authenticated
def delete_user(user_id):
  if user := User.query.filter_by(id=user_id).first():
    return user_schema.dump(user.delete())

  return create_error('User not found!', 404)