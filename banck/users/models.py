from datetime import datetime
from banck import db


class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  created_at = db.Column(db.DateTime, default=datetime.now())
  admin = db.Column(db.Boolean, default=False)
  name = db.Column(db.String(30), nullable=False)
  last_name = db.Column(db.String(30), nullable=False)
  email = db.Column(db.String(100), nullable=False)
  password = db.Column(db.String(60), nullable=False)
  balance = db.Column(db.Integer, default=0)


  def __init__(self, name, last_name, email, password):
    self.name = name
    self.last_name = last_name
    self.email = email
    self.password = password


  def add(self):
    db.session.add(self)
    db.session.commit()

    return self


  def update(self):
    db.session.commit()

    return self


  def delete(self):
    db.session.delete(self)
    db.session.commit()

    return self


  def exists(self):
    return True if User.query.filter_by(email=self.email).first() else False


  def __repr__(self):
    return f'User({self.id}, {self.email})'