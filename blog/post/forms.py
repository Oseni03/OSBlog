from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from blog.models import User, Post, Comment, Executives, Category
from flask_login import current_user


class CreatePostForm(FlaskForm):
  title = StringField("Title", 
          validators=[DataRequired()])
  content = TextAreaField("Content", 
            validators=[DataRequired()])
  category = SelectMultipleField("Category", choices=[
    (cat.id, f"{cat.name}") 
    for cat in Category.query.order_by(Category.id).all()])
  picture = FileField("Add Image", validators=[FileAllowed(["jpg", "mp4", "png"])])
  submit = SubmitField("Post")
  
  
class CommentForm(FlaskForm):
  name = StringField("Name", validators=[DataRequired()])
  email = StringField("Email", validators=[DataRequired(), Email()])
  comment = TextAreaField("Add comment", validators=[DataRequired()])
  submit = SubmitField("Submit")
  

