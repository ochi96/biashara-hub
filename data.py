import os
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, session, abort, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import LoginForm,SignUpForm
from config import Config

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "userdatabase.db"))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config.from_object(Config)

db = SQLAlchemy(app)
db.create_all()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(64), index=True, unique=True)
        email = db.Column(db.String(120), index=True, unique=True)
        password_hash = db.Column(db.String(128))
        posts = db.relationship('Post', backref='author', lazy='dynamic')

        def __repr__(self):
                return '<User {}>'.format(self.username)

class Post(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        body = db.Column(db.String(140))
        timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

        def __repr__(self):
                return '<Post {}>'.format(self.body)

class Customer(User):
        @app.route("/")
        def index():
                form = LoginForm()
                return render_template("index.html",form=form)
        
        @app.route("/dashboard")  ###redirects and url for() improvements
        def dashboard():
                return render_template("dashboard1.html")

        
        @app.route('/login', methods=['GET','POST'])
        def login():           ##form validators,flash messages,, improve error validation on login forms
                form = LoginForm()
                for user in User.query.all():
                        if request.form['password'] ==user.password and request.form['username'] == user.username:
                                flash('Welcome {}'.format(user.username))
                                return render_template("dashboard1.html")
                else:
                        return render_template('index1.html',form=form)

        @app.route('/signup',methods=['GET','POST'])
        def signup():
                return render_template("index2.html")
        
        @app.route('/sign up',methods=['GET','POST'])
        def signupcustorbiz():
                form=SignUpForm
                return render_template('index3.html',form=form)


        @app.route('/sign up client',methods=['GET','POST'])
        def Customer_signup():
                if request.form:
                        form=SignUpForm
                        if request.form['password'] != request.form['password2']:
                                return render_template('index3.html')
                        else:
                                user = User(username=request.form["username"],password=request.form["password"],email=request.form['email'],location=request.form['location'])
                                db.session.add(user)
                                db.session.commit()
                                return render_template('dashboard1.html')

        @app.route("/logout")
        def logout():
                form = LoginForm()       
                return render_template("index.html",form=form)





