import secrets
import os 
from PIL import Image
from flask import render_template, redirect, url_for, flash, abort, Blueprint, request
from blog import app, db 
from blog.user.forms import UpdateAccountForm
from blog.models import User, Post, Category, Comment, PostCategory
from flask_login import login_user, current_user, logout_user, login_required

user = Blueprint('user', __name__,
    template_folder='/templates',
    static_folder='/static', static_url_path='assets')  
    
def secure_filename(filename):
  random_hex = secrets.token_hex(8)
  _, f_ext = os.path.splitext(filename.filename)
  picture_fn = random_hex + f_ext
  
  output_size = (125, 125)
  i= Image.open(filename)
  i.thumbnail(output_size)
  i.save(os.path.join(app.config['UPLOAD_FOLDER'], picture_fn))
  
  return picture_fn
    
@user.route("/update", methods=['GET', 'POST'])
@login_required
def update_user():
  form=UpdateAccountForm()
  if form.validate_on_submit():
    user=User(
      first_name=form.first_name.data,
      last_name=form.last_name.data,
      email=form.email.data,
      image_file=form.picture.data
      )
    db.session.add(user)
    db.session.commit()
    flash("Account updated successfully", "success")
    return redirect(url_for(""))
  return render_template("update_user.html")

    
@user.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
  posts=Post.query.filter_by(author=current_user).order_by(Post.date_posted.desc()).all()
  comment_no=0
  
  form=UpdateAccountForm()
  if form.validate_on_submit():
    picture=None
    if form.picture.data:
      picture=secure_filename(form.picture.data)
    
    current_user.first_name=form.first_name.data
    current_user.last_name=form.last_name.data
    current_user.email=form.email.data
    if picture!=None:
      current_user.image_file=picture
    db.session.commit()
    flash("Account updated successfully", "success")
    return redirect(url_for("auth.home"))

  elif request.method == "GET":
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.email.data=current_user.email
   
    
  return render_template("profile.html", posts=posts, form=form, comment_no=comment_no)