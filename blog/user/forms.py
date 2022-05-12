from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class UpdateAccountForm(FlaskForm):
  first_name = StringField("First Name", 
            validators=[DataRequired()])
  last_name = StringField("Last Name", 
            validators=[DataRequired()])
  email = StringField("Email",
          validators=[DataRequired(), Email()])
  picture = FileField("Update profile picture", validators=[FileAllowed(["jpg", "png"])])
  submit = SubmitField("Update")

      
  def validate_email(self, email):
    if email.data != current_user.email:
      user = User.query.filter_by(email=email.data).first()
      if user:
        raise ValidationError("That email already exist!")
        