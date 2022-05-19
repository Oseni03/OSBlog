import secrets, os
from flask import render_template, redirect, url_for, flash, abort, Blueprint, request
from blog import app, db, mail
from blog.models import (
  User, Post, Category, PostCategory, 
  Comment, Contact, ResetCodes)
from blog.auth.forms import RegistrationForm, LoginForm, ContactForm, AdminUserCreateForm, AdminUserUpdateForm, SearchForm, RequestResetForm, ResetPasswordForm, ConfirmTokenForm
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message


def send_mail(to, subject, template, **kwargs):
  msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
  msg.body = render_template(template, **kwargs)
  msg.html = render_template(template, **kwargs)
  mail.send(msg)


auth = Blueprint('auth', __name__,
    template_folder='/templates',
    static_folder='/static', static_url_path='assets')  
  
  
@auth.route("/register", methods=["GET", "POST"])
def register():
  if current_user.is_authenticated:
    return redirect(url_for("auth.home"))
  form = RegistrationForm()
  if form.validate_on_submit():
    hash_password = generate_password_hash(form.password.data)
    user = User(
      first_name=form.first_name.data, 
      last_name=form.last_name.data, 
      email=form.email.data, 
      password=hash_password)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    flash("Account created successfully", "success")
    return redirect(url_for("auth.home"))
  return render_template("register.html", form=form)
  
  
@auth.route("/login", methods=["GET", "POST"])
def login():
  if current_user.is_authenticated:
    return redirect(url_for("auth.home"))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and user.verify_password(form.password.data):
      flash("Login successful", "success")
      login_user(user)
      return redirect(url_for("auth.home"))
    else:
      flash("Invalid credentials", "danger")
  return render_template("login.html", form=form)
  
  
@auth.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for("auth.home"))
  
  
@auth.route("/")
@auth.route("/home", methods=["GET", "POST"])
def home():
  page = request.args.get("page", 1, type=int)
  
  posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=15)
  form=SearchForm()
  if form.validate_on_submit():
    search_word=form.search.data
    if search_word:
      posts=Post.query.filter(Post.title.like("%" + search_word + "%")).all().paginate(page=page, per_page=15)
    
  return render_template("home.html", posts=posts, form=form, title="Home 🏡 age", paging=posts)
  
  
@auth.route("/about")
def about():
  return render_template("about.html")
  
  
@auth.route("/contact", methods=["GET", "POST"])
def contact():
  form = ContactForm()
  if form.is_submitted():
    contact=Contact(name=form.name.data, email=form.email.data, subject=form.subject.data, message=form.message.data)
    db.session.add(contact)
    db.session.commit()
    flash("Message sent successfully", "success")
    return redirect(url_for("auth.home"))
  return render_template("contact.html", form=form)
    

@auth.route('/create_admin', methods=['GET', 'POST'])
#@login_required
def create_admin():
  form = AdminUserCreateForm()
  if form.validate_on_submit():
    hash_password = generate_password_hash(form.password.data)
    user = User(
      first_name=form.first_name.data, 
      last_name=form.last_name.data, 
      email=form.email.data, 
      password=hash_password,
      admin=form.admin.data)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    flash("Account created successfully", "success")
    return redirect(url_for("auth.home"))
  return render_template("register_admin.html", form=form)


def send_reset_password_instructions(user):
    """Sends the reset password instructions email for the specified user.

    :param user: The user to send the instructions to
    """
    code = secrets.token_hex(6)
    
    # reset_link = url_for_security('reset_password', token=token, _external=True)
    send_mail(user.email, 
      'Password Reset Code', 
      "mail/reset_instructions.html", 
      code=code)
    reset = ResetCodes(user_id=user.id, code=code)
    db.session.add(reset)
    db.session.commit()
    
def send_password_reset_notice(user):
    """Sends the password reset notice email for the specified user.
    :param user: The user to send the notice to
    """
    send_mail(user.email, "Reset Notice", 'mail/reset_notice.html', user=user)
  

@auth.route('/reset_request', methods=['GET', 'POST'])
def reset_request():
  form=RequestResetForm()
  if form.validate_on_submit():
    user=User.query.filter_by(email=form.email.data).first()
    send_reset_password_instructions(user)
    send_password_reset_notice(user)
    flash("Password reset instructions has been sent to your email", "info")
    return redirect(url_for("auth.confirm_reset_code", user_id=user.id))
  
  return render_template("password_reset_request.html", form=form)
  
  
@auth.route('/confirm_code/<int:user_id>', methods=['GET', 'POST'])
def confirm_reset_code(user_id):
  user=User.query.get_or_404(user_id)
  form=ConfirmTokenForm()
  
  if form.validate_on_submit():
    code = ResetCodes.query.filter(ResetCodes.user==user, ResetCodes.code==form.code.data, ResetCodes.used==False).first()
    if code:
      code.mark_used()
      return redirect(url_for("auth.password_reset", user_id=user.id))
    
    # status = code.code_status(form.code.data, user)
    
    # if status == "Invalid":
    #   flash("Invalid token", "warning")
    #   return redirect(url_for("auth.confirm_reset_code", user_id=user.id))
    # elif status == "Expired":
    #   flash("Expired token", "warning")
    #   return redirect(url_for("auth.reset_request"))
    # elif status == "Valid":
    #   ResetCodes.mark_used(form.code.data, user)
    #   return redirect(url_for("auth.password_reset", user_id=user.id))
  return render_template("confirm_code.html", form=form)
  
  
@auth.route('/reset_password/<int:user_id>', methods=['GET', 'POST'])
def password_reset(user_id):
  form=ResetPasswordForm()
  user=User.query.get_or_404(user_id)
  if form.validate_on_submit():
    user.password=generate_password_hash(form.password.data)
    db.session.commit()
    send_password_reset_notice(user)
    login_user(user)
    flash("Password reset successful", "success")
    return redirect(url_for("auth.home"))
  return render_template("password_reset.html", form=form)
    
