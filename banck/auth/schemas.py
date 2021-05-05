from banck import ma
from marshmallow import fields


class LoginSchema(ma.Schema):
  email = fields.Str(required=True)
  password = fields.Str(required=True)


login_schema = LoginSchema()