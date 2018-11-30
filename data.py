import os
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, session, abort, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager,UserMixin, current_user, login_user, logout_user, login_required


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email,EqualTo

from config import Config

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "userdatabase.db"))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'

db = SQLAlchemy(app)
db.create_all()
migrate = Migrate(app, db)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(64), index=True, unique=True)
        email = db.Column(db.String(120), index=True, unique=True)
        password_hash = db.Column(db.String(128))
        posts = db.relationship('Post', backref='author', lazy='dynamic')

        def __repr__(self):
                return '<User {}>'.format(self.username)
        
        def set_password(self, password):
                self.password_hash = generate_password_hash(password)

        def check_password(self, password):
                return check_password_hash(self.password_hash, password)

class Post(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        body = db.Column(db.String(140))
        timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

        def __repr__(self):
                return '<Post {}>'.format(self.body)

class RegistrationForm(FlaskForm):
        username = StringField('Username', validators=[DataRequired()])
        email = StringField('Email', validators=[DataRequired(), Email()])
        password = PasswordField('Password', validators=[DataRequired()])
        password2 = PasswordField(
                'Repeat Password', validators=[DataRequired(), EqualTo('password')])
        submit = SubmitField('Register')

        def validate_username(self, username):
                user = User.query.filter_by(username=username.data).first()
                if user is not None:
                        raise ValidationError('Please use a different username.')

        def validate_email(self, email):
                user = User.query.filter_by(email=email.data).first()
                if user is not None:
                        raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
        username = StringField('Username', validators=[DataRequired()])
        password = PasswordField('Password', validators=[DataRequired()])
        remember_me = BooleanField('Remember Me')
        submit = SubmitField('Sign In')

class Customer(User):
        @app.route("/")
        @login_required         ###redirects and url for() improvements
        def index():
                return render_template("dashboard1.html")
        
        @app.route("/dashboard")  ###redirects and url for() improvements
        def dashboard():
                return render_template("dashboard1.html")

        
        @app.route('/login', methods=['GET','POST'])
        def login():           ##form validators,flash messages,, improve error validation on login forms
                if current_user.is_authenticated:
                        return render_template("dashboard1.html")
                form = LoginForm()
                if form.validate_on_submit():
                        user = User.query.filter_by(username=form.username.data).first()
                        if user is None or not user.check_password(form.password.data):
                                flash('Invalid username or password')
                                return render_template("index.html",form=form)
                        login_user(user, remember=form.remember_me.data)
                        return render_template("dashboard1.html")
                return render_template('index.html', title='Sign In', form=form)

        
        @app.route('/sign up',methods=['GET','POST'])
        def signupcustorbiz():
                form=RegistrationForm()
                return render_template('index3.html',form=form)

        @app.route('/sign_up_client', methods=['GET','POST'])
        def register():
                if current_user.is_authenticated:
                        return redirect(url_for('dashboard'))
                form = RegistrationForm()
                if form.validate_on_submit():
                        user = User(username=form.username.data, email=form.email.data)
                        user.set_password(form.password.data)
                        db.session.add(user)
                        db.session.commit()
                        
                        flash('Congratulations, you are now a registered user!')
                        return render_template('dashboard1.html')
                return render_template('index3.html', form=form)

        @app.route('/logout')
        def logout():
                logout_user()
                return render_template("dashboard1.html")




