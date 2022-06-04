from blog import app, db, mail
from flask_mail import Message
from blog.models import User
from flask import url_for, render_template


def send_mail(to, subject, template, **kwargs):
  msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
  msg.body = render_template(template, **kwargs)
  msg.html = render_template(template, **kwargs)
  mail.send(msg)
  
  
def send_reset_password_instructions(user):
    """Sends the reset password instructions email for the specified user.
    :param user: The user to send the instructions to
    """
    token = user.get_reset_token(user.id)
    
    reset_link = url_for('auth.password_reset', token=token, _external=True)
    send_mail(user.email, 
      'Password Reset Code', 
      "mail/reset_instructions.html", 
      reset_link=reset_link)
    
def send_password_reset_notice(user):
    """Sends the password reset notice email for the specified user.
    :param user: The user to send the notice to
    """
    send_mail(user.email, "Reset Notice", 'mail/reset_notice.html', user=user)
    
    
def confirm_token(token):
    user_id = User.verify_reset_token(token)
    return user_id