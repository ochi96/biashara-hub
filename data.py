import os

from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask_sqlalchemy import SQLAlchemy


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "userdatabase.db"))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_file


db = SQLAlchemy(app)
db.create_all()


class User(db.Model): ########Database Class for customers#######
        id = db.Column('User_id', db.Integer, primary_key = True)
        username = db.Column(db.String(80), unique=True, nullable=False, primary_key=False)
        password = db.Column(db.String(120), unique=False, nullable=False,primary_key=False)
        email = db.Column(db.String(120), unique=False, nullable=False,primary_key=False)
        location = db.Column(db.String(120), unique=False, nullable=False,primary_key=False)

        def __repr__(self):
                return "<User: {}>".format(self.username)

class Customer(User):
        @app.route("/")
        def index():
                return render_template("index.html")
        
        @app.route("/dashboard")
        def dashboard():
                return render_template("dashboard1.html")

        
        @app.route('/login', methods=['GET','POST'])
        def login():
                for user in User.query.all():
                        if request.form['password'] ==user.password and request.form['username'] == user.username:
                                return render_template("dashboard1.html")
                else:
                        return render_template('index1.html')

        @app.route('/signup',methods=['GET','POST'])
        def signup():
                return render_template("index2.html")
        
        @app.route('/sign up',methods=['GET','POST'])
        def signupcustorbiz():
                return render_template('index3.html')


        @app.route('/sign up client',methods=['GET','POST'])
        def Customer_signup():
                if request.form:
                        if request.form['password'] != request.form['password2']:
                                return render_template('index3.html')
                        else:
                                user = User(username=request.form["username"],password=request.form["password"],email=request.form['email'],location=request.form['location'])
                                db.session.add(user)
                                db.session.commit()
                                return render_template('dashboard1.html')

        @app.route("/logout")
        def logout():        
                return render_template("index.html")





