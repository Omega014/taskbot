from datetime import datetime
from apps.database import db

from flask_login import UserMixin


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    ctime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    utime = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def get_id(self):
        return 1


class Question(db.Model):

    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    ctime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    utime = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


class Answer(db.Model):

    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer)
    text = db.Column(db.String(255), nullable=False)
    ctime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    utime = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
