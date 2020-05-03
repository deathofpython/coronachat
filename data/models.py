import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from hashing import hash_algorythm
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'Users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    last_seen = sqlalchemy.Column(sqlalchemy.String)

    def check_password(self, password):
        if self.hashed_password == hash_algorythm(password):
            return True
        else:
            return False


class Form(FlaskForm):
    username = StringField('Enter username', validators=[DataRequired()])
    password = StringField('Enter password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Chat(SqlAlchemyBase, UserMixin):
    __tablename__ = 'Chats'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    pair = sqlalchemy.Column(sqlalchemy.String)
    data = sqlalchemy.Column(sqlalchemy.String)
