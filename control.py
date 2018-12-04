

from flask import Flask, flash, redirect, render_template, request, session, abort, url_for,flash
from datetime import datetime

from flask_login import LoginManager,UserMixin, current_user, login_user, logout_user, login_required

from config import Config
from forms import RegistrationForm,LoginForm,EditProfileForm,RegisterBusinessForm
from models import app,User,Business,db
login = LoginManager(app)
login.login_view = 'login'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


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



