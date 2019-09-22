from biashara import app

from flask import Flask

import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager,UserMixin, current_user, login_user, logout_user, login_required
from hashlib import md5
from datetime import datetime
from config import Config

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "userdatabase.db"))


app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config.from_object(Config)

db = SQLAlchemy(app)
db.create_all()
migrate = Migrate(app, db)


class User(UserMixin, db.Model): ###exhibits self referential relationship###
        id = db.Column(db.Integer, primary_key=True)
        first_name = db.Column(db.String(64), index=True)
        middle_name = db.Column(db.String(64), index=True)
        username = db.Column(db.String(64), index=True, unique=True)
        age = db.Column(db.Integer, index=True)
        email = db.Column(db.String(120), index=True, unique=True)
        location = db.Column(db.String(100), index=True)
        gender = db.Column(db.String(30), index=True)
        preference = db.Column(db.String(30), index=True)
        profilepicture = db.Column(db.String,default=None, nullable=True)
        image_url = db.Column(db.String,default=None, nullable=True)
        password_hash = db.Column(db.String(128))
        about_me = db.Column(db.String(140))
        last_seen = db.Column(db.DateTime, default=datetime.utcnow)

        def __repr__(self):
                return '<User {}>'.format(self.username)
        
        def set_password(self, password):
                self.password_hash = generate_password_hash(password)

        def check_password(self, password):
                return check_password_hash(self.password_hash, password)
        
        def avatar(self, size):
                digest = md5(self.email.lower().encode('utf-8')).hexdigest()
                return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


class Matches(db.Model):
        id = db.Column(db.Integer, primary_key=True,index=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        feedback = db.Column(db.String(200))
        timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
        
        def __repr__(self):
                return 'Match: {}'.format(self.feedback)





