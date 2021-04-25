from banck import ma
from .models import User


class UserSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = User


class UserCreationSchema(ma.SQLAlchemySchema):
  class Meta:
    model = User

  name = ma.auto_field()
  last_name = ma.auto_field()
  email = ma.auto_field()
  password = ma.auto_field()


user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_creation_schema = UserCreationSchema()