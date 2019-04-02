

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField, SelectField
from wtforms.validators import ValidationError, Email, EqualTo , Length, DataRequired
from biashara.models import User,Business,Reviews
from biashara import app

locations = [('Nairobi','Nairobi'),('Mombasa','Mombasa'),('Kisumu','Kisumu'),('Nakuru','Nakuru'),('Nyeri','Nyeri')]
categories = [('Agriculture','Agriculture'),('Military','Military'),('Trade','Trade'),('Entertainment','Entertainment'),('Technology','Technology'),('Dating','Dating')]
genders = [('Female','Female'),('Male','Male')]
preferences = [('Male','Male'),('Female','Female')]
years = [('1933', '1933'), ('1934', '1934'), ('1935', '1935'), ('1936', '1936'), ('1937', '1937'), ('1938', '1938'),
        ('1939', '1939'), ('1940', '1940'), ('1941', '1941'), ('1942', '1942'), ('1943', '1943'), ('1944', '1944'),
        ('1945', '1945'), ('1946', '1946'), ('1947', '1947'), ('1948', '1948'), ('1949', '1949'), ('1950', '1950'),
        ('1951', '1951'), ('1952', '1952'), ('1953', '1953'), ('1954', '1954'), ('1955', '1955'), ('1956', '1956'),
        ('1957', '1957'), ('1958', '1958'), ('1959', '1959'), ('1960', '1960'), ('1961', '1961'), ('1962', '1962'), 
        ('1963', '1963'), ('1964', '1964'), ('1965', '1965'), ('1966', '1966'), ('1967', '1967'), ('1968', '1968'),
        ('1969', '1969'), ('1970', '1970'), ('1971', '1971'), ('1972', '1972'), ('1973', '1973'), ('1974', '1974'),
        ('1975', '1975'), ('1976', '1976'), ('1977', '1977'), ('1978', '1978'), ('1979', '1979'), ('1980', '1980'),
        ('1981', '1981'), ('1982', '1982'), ('1983', '1983'), ('1984', '1984'), ('1985', '1985'), ('1986', '1986'),
        ('1987', '1987'), ('1988', '1988'), ('1989', '1989'), ('1990', '1990'), ('1991', '1991'), ('1992', '1992'),
        ('1993', '1993'), ('1994', '1994'), ('1995', '1995'), ('1996', '1996'), ('1997', '1997'), ('1998', '1998'),
        ('1999', '1999'), ('2000', '2000'), ('2001', '2001')]



class RegistrationForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired(),Length(min=2,max=30,message='Enter appropriate First Name')])
    middle_name = StringField('Middle name', validators=[DataRequired(),Length(min=2,max=30,message='Enter appropriate Middle Name')])
    username = StringField('Username', validators=[DataRequired()])
    age = SelectField('Year of Birth', validators=[DataRequired()],choices=years)
    email = StringField('Email', validators=[DataRequired(), Email()])
    location = StringField('Town/City:', validators=[DataRequired()])
    gender = SelectField('Sex/Gender',validators=[DataRequired()],choices=genders)
    preference = SelectField('Interested in:',validators=[DataRequired()],choices=preferences)
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                    raise ValidationError('Please use a different username. Username already exists')

    def validate_email(self, email):
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                    raise ValidationError('Please use a different email address. Email address already exists')

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
    businessname = StringField('Business name', validators=[DataRequired()])
    about_business = TextAreaField('About the business', validators=[Length(min=0, max=200)])
    location = SelectField('Location', choices=locations)
    category = SelectField('Category', choices=categories)
    submit = SubmitField('Submit')
    
class CriteriaForm(FlaskForm):
    location = SelectField('Location', choices=locations)
    category = SelectField('Category', choices=categories)
    submit = SubmitField('Submit')

class ReviewsForm(FlaskForm):
    feedback = TextAreaField('Write your Review', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')





