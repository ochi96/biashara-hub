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
        username = db.Column(db.String(64), index=True, unique=True)
        email = db.Column(db.String(120), index=True, unique=True)
        password_hash = db.Column(db.String(128))
        about_me = db.Column(db.String(140))
        last_seen = db.Column(db.DateTime, default=datetime.utcnow)
        businesses = db.relationship('Business', backref='User', lazy='dynamic')

        def __repr__(self):
                return '<User {}>'.format(self.username)
        
        def set_password(self, password):
                self.password_hash = generate_password_hash(password)

        def check_password(self, password):
                return check_password_hash(self.password_hash, password)
        
        def avatar(self, size):
                digest = md5(self.email.lower().encode('utf-8')).hexdigest()
                return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


class Business(db.Model):
        id = db.Column(db.Integer, primary_key=True,index=True)
        businessname=db.Column(db.String(64), index=True, unique=True)
        about_business=db.Column(db.String(200))
        location=db.Column(db.String(200))
        category=db.Column(db.String(200))
        timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

        def __repr__(self):
                return 'Business: {}'.format(self.businessname)

class Reviews(db.Model):
        id = db.Column(db.Integer, primary_key=True,index=True)
        feedback = db.Column(db.String(200))
        business_id = db.Column(db.Integer, db.ForeignKey('business.id'))
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
        
        def __repr__(self):
                return 'Review: {}'.format(self.feedback)





