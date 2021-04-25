from flask import Blueprint, jsonify, request
from .models import User
from .schemas import user_schema, users_schema, user_creation_schema
from banck.utils import create_error


users = Blueprint('users', __name__)


@users.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
  if user := User.query.filter_by(id=user_id).first():
    return user_schema.dump(user)

  return create_error('User not found!', 404)


@users.route('/api/users', methods=['GET'])
def get_users():
  return jsonify(users_schema.dump(User.query.all()))


@users.route('/api/users', methods=['POST'])
def create_user():
  if error := user_creation_schema.validate(request.json):
    return create_error(error, 400)

  user = User(
    request.json['name'],
    request.json['last_name'],
    request.json['email'],
    request.json['password']
  )
  if user.exists():
    return create_error('User already exists!', 409)

  user.add()

  return user_schema.dump(user)


@users.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
  if user := User.query.filter_by(id=user_id).first():
    if 'name' in request.json:
      user.name = request.json['name']
    if 'last_name' in request.json:
      user.last_name = request.json['last_name']
    if 'email' in request.json:
      user.email = request.json['email']
    if 'password' in request.json:
      user.password = request.json['password']
    if 'balance' in request.json:
      user.balance = request.json['balance']

    return user_schema.dump(user.update())

  return create_error('User not found!', 404)


@users.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
  if user := User.query.filter_by(id=user_id).first():
    return user_schema.dump(user.delete())

  return create_error('User not found!', 404)