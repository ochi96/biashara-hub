
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for,flash
from datetime import datetime
from flask_login import LoginManager,UserMixin, current_user, login_user, logout_user, login_required
from config import Config
from biashara.forms import RegistrationForm,LoginForm,EditProfileForm,RegisterBusinessForm,CriteriaForm,ReviewsForm
from biashara.models import app,User,Business,db,Reviews

from biashara import app
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
                return render_template('update_profile.html')
        elif request.method == 'GET':
                form.username.data = current_user.username
                form.about_me.data = current_user.about_me
        return render_template('about.html',form=form,username=current_user.username)


@app.route('/update_profile',methods=['GET','POST'])
@login_required
def update_profile():
        return render_template('update_profile.html')



@app.route('/register_biz',methods=['GET','POST'])
@login_required
def register_business():
        form=RegisterBusinessForm()
        if form.validate_on_submit():
                business=Business(businessname = form.businessname.data,about_business = form.about_business.data,
                location=form.location.data,category=form.category.data,user_id=current_user.id)
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
                business.location=form.location.data
                business.category=form.category.data
                db.session.commit()
                return render_template('update_profile.html',form=form)
        elif request.method == 'GET':
                form.businessname.data = business.businessname
                form.about_business.data = business.about_business
                form.location.data = business.location
                form.category.data = business.category
        return render_template('register2.html', title='Edit Profile',form=form,business=business)

@app.route('/updated_business',methods=['GET','POST'])
def updated_business():
        form=RegisterBusinessForm()
        if form.validate_on_submit():
                db.session.commit()
                return render_template('update_profile.html',form=form)

        

@app.route('/delete_business<businessname>',methods=['GET','POST'])
@login_required
def delete_business(businessname):
        business=Business.query.filter_by(businessname=businessname).all()
        for business in business:
                db.session.delete(business)
                db.session.commit()
                return render_template('live2.html',business=business)


@app.route('/all_businessess',methods=['GET','POST'])
@login_required
def all_businesses():
        all_businesses=Business.query.all()
        return render_template('all_businesses.html',all_businesses=all_businesses)

##searching
@app.route('/business_profiles<businessname>')
@login_required
def business_profiles(businessname):
        business=Business.query.filter_by(businessname=businessname).first_or_404()
        return render_template('business_profile.html',business=business)


@app.route('/criteria',methods=['GET','POST'])
@login_required
def Criteria():
        form = CriteriaForm()
        businesses=Business.query.all()
        return render_template('search.html',form=form,businesses=businesses)

@app.route('/search_results',methods=['GET','POST'])
@login_required
def search_results():
        form = CriteriaForm()
        businesses=Business.query.all()
        if form.validate_on_submit:
                return render_template('search_results.html',form=form,businesses=businesses)

                
####reviews
@app.route('/review<id>',methods=['GET','POST'])
@login_required
def review(id):
        form=ReviewsForm()
        business= Business.query.filter_by(id=id).first_or_404()
        if request.method=='GET':
                return render_template('reviews.html',form=form)

        elif form.validate_on_submit:
                review = Reviews(feedback=form.feedback.data,user_id=current_user.id,business_id=business.id)
                db.session.add(review)
                db.session.commit()
                return render_template('update_profile.html')
        
        return render_template('reviews.html',form=form)


@app.route('/review_business',methods=['GET','POST'])
@login_required
def review_business():
        return render_template('update_profile.html')

'''
@app.route('/view_reviews',methods=['GET','POST'])
@login_required
def view_reviews():
        pass
'''    
        






