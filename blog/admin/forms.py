from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from blog.models import User, Post, Comment, Executives, Category, PostCategory 

  
class ExecutiveForm(FlaskForm):
  user = SelectField("Select User", coerce=int, choices=[
    (user.id, f"{user.first_name} {user.last_name}") 
    for user in User.query.order_by(User.id).all()])
  post = StringField("Post", validators=[DataRequired()])
  submit = SubmitField("Add")
  

class CategoryForm(FlaskForm):
  name = StringField("Name", validators=[DataRequired()])  
  submit = SubmitField("Add")
  
class ContactForm(FlaskForm):
  name = StringField("Name", validators=[DataRequired()])
  email = StringField("Email", validators=[DataRequired(), Email()])
  subject = StringField("Subject", validators=[DataRequired()])
  message = TextAreaField("Message", validators=[DataRequired()])
  submit = SubmitField("Submit")
  
class SetRead(FlaskForm):
  read = SubmitField("Read")