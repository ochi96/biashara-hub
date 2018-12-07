

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email,EqualTo ,Length
from biashara.models import User,Business,Reviews
from biashara import app

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
    location = SelectField('Location', choices=locations)
    category = SelectField('Category', choices=categories)
    submit = SubmitField('Submit')
    
class CriteriaForm(FlaskForm):
    #picks = [('location','location')('category','category')]
    locations = [('Nairobi','Nairobi'),('Mombasa','Mombasa'),('Kisumu','Kisumu'),('Nakuru','Nakuru')]
    categories = [('Agriculture','Agriculture'),('Military','Military'),('Trade','Trade'),('Entertainment','Entertainment'),('Technology','Technology')]
    location = SelectField('Location', choices=locations)
    category = SelectField('Category', choices=categories)
    submit = SubmitField('Submit')

class ReviewsForm(FlaskForm):
    feedback = TextAreaField('Write your Review', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')




