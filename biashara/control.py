
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for,flash
import os
from werkzeug import secure_filename
from datetime import datetime
from flask_login import LoginManager,UserMixin, current_user, login_user, logout_user, login_required
from flask_uploads import UploadSet, IMAGES, configure_uploads
import subprocess



from config import Config
from biashara.forms import RegistrationForm,LoginForm,EditProfileForm,CriteriaForm,ReviewsForm,MatchesForm
from biashara.models import app,User,db,Matches


from biashara import app
login = LoginManager(app)
login.login_view = 'login'
images = UploadSet('images',IMAGES)
configure_uploads(app,images)



@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/")
@login_required         ###redirects and url for() improvements
def index():
        form = LoginForm()
        return render_template("twitterexample.html",form=form)              #should be loginpage.html


@app.route("/log in",methods=['GET','POST'])  ###redirects and url for() improvements
def loginsheets():
        form = LoginForm()
        return render_template("loginpage.html",form=form)


@app.route('/log_in_client', methods=['GET','POST'])
def login():           ##form validators,flash messages,, improve error validation on login forms
        if current_user.is_authenticated:
                return render_template("dashboard2.html")
        form = LoginForm()
        if form.validate_on_submit():
                user = User.query.filter_by(username=form.username.data).first()
                if user is None or not user.check_password(form.password.data):
                        flash('Invalid username or password')
                        return render_template("loginpage.html",form=form)
                login_user(user, remember=form.remember_me.data)
                return render_template("dashboard2.html")                  #shd be dashboard2.html
        return render_template('loginpage.html', title='Sign In', form=form)



@app.route('/sign up',methods=['GET','POST'])
def signupsheets():
        form=RegistrationForm()
        return render_template('index3.html',form=form)

@app.route('/sign_up_client', methods=['GET','POST'])
def signup():
        if current_user.is_authenticated:
                return redirect(url_for('dashboard'))
        form = RegistrationForm()
        if form.validate_on_submit():
                age=2019-int(form.age.data)
                profilepicture = form.profilepicture.data
                filename = images.save(request.files['profilepicture'])
                url = images.url(filename)
                user = User(first_name = form.first_name.data,middle_name = form.middle_name.data,
                username = form.username.data,age=age, email = form.email.data, location = form.location.data,
                gender = form.gender.data, preference = form.preference.data, profilepicture=filename,image_url=url)
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.commit()
                return render_template('dashboard1.html')
        return render_template('index3.html', form=form)



@app.route('/logout')
@login_required
def logout():
        logout_user()
        return render_template("logout.html")


@app.route('/userprofileview/<username>')
@login_required
def userprofileview(username):
        user = User.query.filter_by(username=username).first_or_404()
        return render_template('profile.html', user=user)


@app.before_request
def before_request():
        if current_user.is_authenticated:
                current_user.last_seen = datetime.utcnow()
                db.session.commit()



@app.route('/update_profile',methods=['GET','POST'])
@login_required
def update_profile():
        return render_template('update_profile.html')

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
        form = EditProfileForm()
        if form.validate_on_submit():
                current_user.username = form.username.data
                current_user.about_me = form.about_me.data
                db.session.commit()
                return render_template('update_profile.html')
        elif request.method == 'GET':
                form.username.data = current_user.username
                form.about_me.data = current_user.about_me
        return render_template('aboutme.html',form=form,username=current_user.username)





#@app.route('/your_live_business')
#def current_business():
        #running_businesses=Business.query.filter_by(user_id=current_user.id).all()
        #Sreturn render_template('livebusiness.html',running_businesses=running_businesses)

@app.route('/potential_matches',methods=['GET','POST'])
@login_required
def all_businesses():
        all_businesses=User.query.all()
        return render_template('potential_matches.html',all_businesses=all_businesses)


@app.route('/criteria',methods=['GET','POST'])
@login_required
def Criteria():
        form = CriteriaForm()
        matches=User.query.all()
        return render_template('search.html',form=form,matches=matches)


@app.route('/new_match',methods=['GET','POST'])
def sending_likes():
        form = MatchesForm()
        if form.validate_on_submit:
                liking= Matches(user_id=current_user.id)
                db.session.add(liking)
                db.session.commit()
                return render_template('reviewed.html')
        
        return render_template('update_profile.html')


#python3 __init__.py
#<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css" integrity="sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4" crossorigin="anonymous">
        






