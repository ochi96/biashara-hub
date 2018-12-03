import os
from datetime import datetime
from hashlib import md5

from flask import Flask, flash, redirect, render_template, request, session, abort, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager,UserMixin, current_user, login_user, logout_user, login_required


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email,EqualTo ,Length

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

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

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

class EditProfileForm(FlaskForm):
        username = StringField('Username', validators=[DataRequired()])
        about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
        submit = SubmitField('Submit')

class RegisterBusinessForm(FlaskForm):
        locations = [('Nairobi','Nairobi'),('Mombasa','Mombasa'),('Kisumu','Kisumu'),('Nakuru','Nakuru')]
        categories = [('Agriculture','Agriculture'),('Military','Military'),('Trade','Trade'),('Entertainment','Entertainment'),('Technology','Technology')]
        businessname = StringField('Business name', validators=[DataRequired()])
        about_business = TextAreaField('About the business', validators=[Length(min=0, max=200)])
        location=SelectField('Location', choices=locations)
        category=SelectField('Category', choices=categories)
        submit = SubmitField('Submit')


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

        @app.route('/user/<username>')
        @login_required
        def user(username):
                user = User.query.filter_by(username=username).first_or_404()
                return render_template('profile.html', user=user)
        
        @app.before_request
        def before_request():
                if current_user.is_authenticated:
                        current_user.last_seen = datetime.utcnow()
                        db.session.commit()
        
        @app.route('/edit_profile', methods=['GET', 'POST'])
        @login_required
        def edit_profile():
                form = EditProfileForm()
                if form.validate_on_submit():
                        current_user.username = form.username.data
                        current_user.about_me = form.about_me.data
                        db.session.commit()
                        return redirect(url_for('edit_profile'))
                elif request.method == 'GET':
                        form.username.data = current_user.username
                        form.about_me.data = current_user.about_me
                return render_template('about.html', title='Edit Profile',form=form)
        




        
@app.route('/register_biz',methods=['GET','POST'])
@login_required
def register_business():
        form=RegisterBusinessForm()
        if form.validate_on_submit():
                business=Business(businessname = form.businessname.data,about_business = form.about_business.data,
                location=request.form['location'],category=request.form['category'],user_id=current_user.id)
                db.session.add(business)
                db.session.commit()
                return render_template('live.html',business=business)
        return render_template('register.html', title='Edit Profile',form=form)

@app.route('/your_live_business')
def current_business():
        running_businesses=Business.query.filter_by(user_id=current_user.id).all()
        return render_template('livebusiness.html',running_businesses=running_businesses)

@app.route('/update_business<businessname>',methods=['GET','POST'])
def update_business(businessname):
        form=RegisterBusinessForm()
        business=Business.query.filter_by(businessname=businessname).first()
        if form.validate_on_submit():
                business.businessname = form.businessname.data
                business.about_business = form.about_business.data
                business.location=request.form['location']
                business.category=request.form['category']
                db.session.commit()
        elif request.method == 'GET':
                form.businessname.data = business.businessname
                form.about_business.data = business.about_business
                '''request.form['location']=business.location
                request.form['category']=business.category'''

        return render_template('register.html', title='Edit Profile',form=form)
        



#return render_template('register.html', title='Edit Profile',form=form)
@app.route('/delete_biz',methods=['GET','POST'])
@login_required
def delete_business():
        running_businesses=Business.query.filter_by(user_id=current_user.id).all()
        for business in running_businesses:
                db.session.delete(business)
                db.session.commit()
                return render_template('live2.html',business=business)


