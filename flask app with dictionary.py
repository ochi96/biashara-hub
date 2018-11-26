from flask import Flask, flash, redirect, render_template, request, session, abort, url_for

app = Flask(__name__)

Users=[ { 'name':'brams','password':'123'},{ 'name':'queen','password':'456'},{'name':'loise','password':'haha'}]

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard1.html")


@app.route('/login', methods=['POST'])
def login():
    for user in Users:
        if request.form['password'] ==user['password'] and request.form['username'] == user['name']:
                return dashboard()
        else:
                return render_template('index1.html')

@app.route('/signup',methods=['POST'])
def signup():
    return render_template("index2.html")


@app.route('/sign up',methods=['POST'])
def moreusers():
        user={'name':'','password':''}
        if request.form['password'] == request.form['password2']:
                user['name']=request.form['username']
                user['password']=request.form['password']
                Users.append(user)
                print(Users)
                return render_template('dashboard1.html')
        else:
            return render_template('index2.html')

@app.route("/logout")
def logout():        
        return render_template("index.html")
