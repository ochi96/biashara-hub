
def years():
    valid_years=[]
    for year in range(1933,2000):
        valid_years.append(year)
        year=year+1
    x=valid_years
    y=[]
    for x in valid_years:
        k=[]
        z=str(x)
        k.append(z)
        k.append(z)
        y.append(tuple(k))
    print (y)

years()


@app.route('/login2', methods=['GET','POST'])
def signin():           ##form validators,flash messages,, improve error validation on login forms
        if current_user.is_authenticated:
                return render_template("dashboard2.html")
        form = LoginForm()
        if form.validate_on_submit():
                user = User.query.filter_by(username=form.username.data).first()
                if user is None or not user.check_password(form.password.data):
                        flash('Invalid username or password')
                        return render_template("indexalt.html",form=form)
                login_user(user, remember=form.remember_me.data)
                return render_template("dashboard2.html")
        return render_template('index.html', title='Sign In', form=form)

def validate_username(self, username):
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                    raise ValidationError('Please use a different username. Username already exists')