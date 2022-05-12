from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from blog.models import User, Post, Comment, Executives, Category, PostCategory


class RegistrationForm(FlaskForm):
  first_name = StringField("First Name", 
            validators=[DataRequired(), Length(min=2,max=25)])
  last_name = StringField("Last Name", 
            validators=[DataRequired(), Length(min=2,max=25)])
  email = StringField("Email",
          validators=[DataRequired(), Email()])
  password = PasswordField("Password", 
            validators=[DataRequired()])
  confirm_password = PasswordField("Confirm Password", 
            validators=[DataRequired(), EqualTo("password")])
  submit = SubmitField("sign up")
  
      
  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError("This user already exist!")
  
class LoginForm(FlaskForm):
  email = StringField("Email",
          validators=[DataRequired(), Email()])
  password = PasswordField("Password", 
            validators=[DataRequired()])
  remember = BooleanField("Remember me")
  submit = SubmitField("Login")
  

class AdminUserCreateForm(FlaskForm):
  first_name = StringField("First Name", 
            validators=[DataRequired(), Length(min=2,max=25)])
  last_name = StringField("Last Name", 
            validators=[DataRequired(), Length(min=2,max=25)])
  email = StringField("Email",
          validators=[DataRequired(), Email()])
  password = PasswordField("Password", 
            validators=[DataRequired()])
  confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
  admin = BooleanField('Admin ?')
  submit = SubmitField("sign up")
  
  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError("This user already exist!")
  
  
class AdminUserUpdateForm(FlaskForm):
  first_name = StringField("First Name", 
            validators=[DataRequired(), 
            Length(min=2,max=25)])
  last_name = StringField("Last Name", 
            validators=[DataRequired(), 
            Length(min=2,max=25)])
  email = StringField("Email",
          validators=[DataRequired(), 
          Email()])
  admin = BooleanField('Admin ?')
  submit = SubmitField("Update")
  
  
class ContactForm(FlaskForm):
  name = StringField("Name", validators=[DataRequired()])
  email = StringField("Email", validators=[DataRequired(), Email()])
  subject = StringField("Subject", validators=[DataRequired()])
  message = TextAreaField("Message", validators=[DataRequired()])
  submit = SubmitField("Submit")
  
  
class SearchForm(FlaskForm):
  search=StringField("Search", validators=[DataRequired()])
  submit = SubmitField('Go')
  
  
class RequestResetForm(FlaskForm):
  email = StringField("Email",
          validators=[DataRequired()])
  submit = SubmitField("Request Reset Password")
  
  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user == None:
      raise ValidationError("There is no account associated with this email")
      
      
class ResetPasswordForm(FlaskForm):
  password = PasswordField("Password", 
            validators=[DataRequired()])
  confirm_password = PasswordField("Confirm_Password", 
            validators=[DataRequired(), EqualTo("password")])
  submit = SubmitField("Reset Password")
  
  
class ConfirmTokenForm(FlaskForm):
  code = StringField("Enter Code", validators=[DataRequired()])
  submit = SubmitField("Confirm")
  
  
  
#class PasswordlessLoginForm(FlaskForm):
  