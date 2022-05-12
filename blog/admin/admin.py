import secrets, os
from flask import render_template, redirect, url_for, flash, abort, Blueprint, request
from blog import app, db 
from blog.models import User, Post, Category, Executives, Contact
from flask_login import login_user, current_user, logout_user, login_required
from functools import wraps
from blog.admin.forms import ExecutiveForm, CategoryForm, ContactForm
from blog.auth.forms import AdminUserUpdateForm


admin = Blueprint('admin', __name__,
    template_folder='/templates',
    static_folder='/static', static_url_path='assets')
 

@admin.route('/users-list')
@login_required
#@admin_login_required()
def users_list_admin():
  users = User.query.all()
  return render_template('admin_users_list.html', users=users)

  
@admin.route("/add_executive", methods=['GET', 'POST'])
@login_required
def add_executive():
  form=ExecutiveForm()
  if form.validate_on_submit():
    user=User.query.get(form.user.data)
    exco = Executives(exco=user, post=form.post.data)
    db.session.add(exco)
    db.session.commit()
    flash("Executive added successfully", "success")
    return redirect(url_for("admin.users_list_admin"))
  return render_template("add_executive.html", form=form)

  
@admin.route("/add_category", methods=['GET', 'POST'])
@login_required
def add_category():
  form=CategoryForm()
  if form.validate_on_submit():
    category = Category(name=form.name.data)
    db.session.add(category)
    db.session.commit()
    flash("Category added successfully", "success")
    return redirect(url_for("admin.add_category"))
  return render_template("add_category.html", form=form)
  

@admin.route('/update-user/<id>', methods=['GET', 'POST'])
@login_required
def user_update(id):
  user = User.query.get(id)
  form = AdminUserUpdateForm()
  if form.validate_on_submit():
    user.last_name=form.last_name.data,
    user.first_name=form.first_name.data,
    user.email=form.email.data,
    user.admin=form.admin.data 
    db.session.commit()
    flash('User Updated.', 'info')
    return redirect(url_for('auth.users_list_admin'))
    
  elif request.method == "GET":
    form.last_name.data = user.last_name
    form.first_name.data = user.first_name
    form.email.data = user.email
    form.admin.data = user.admin
  return render_template('user_update.html', form=form, user=user)
  
  
@admin.route('/delete-user/<id>', methods=['GET', 'POST'])
@login_required
def user_delete(id):
  user = User.query.get(id)
  db.session.delete(user)
  db.session.commit()
  flash('User Deleted.', "success")
  return redirect(url_for('admin.users_list_admin'))
  
  
@admin.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
  categories=Category.query.all()
  return render_template("categories.html", categories=categories)
  
  
@admin.route('/executives', methods=['GET', 'POST'])
@login_required
def executives():
  executives=Executives.query.all()
  return render_template("executives.html", executives=executives)
  
  
@admin.route('/delete-category/<id>', methods=['GET', 'POST'])
@login_required
def category_delete(id):
  category = Category.query.get(id)
  db.session.delete(category)
  db.session.commit()
  flash('Category Deleted.', "success")
  return redirect(url_for('admin.categories'))
  
  
@admin.route('/delete-executive/<id>', methods=['GET', 'POST'])
@login_required
def executive_delete(id):
  executive = Executives.query.get(id)
  db.session.delete(executive)
  db.session.commit()
  flash('Executive Deleted.', "success")
  return redirect(url_for('admin.executives'))
  

@admin.route("/messages", methods=["GET"])
@login_required
def messages():
  messages=Contact.query.order_by(Contact.id.desc()).all()
  
  for message in messages:
    unread=message.is_not_read()
  return render_template("messages.html", unread=unread, messages=messages)
  
@admin.route("/message/<int:id>/read")
@login_required
def read(id):
  message=Contact.query.get_or_404(id)
  message.read=True 
  db.session.commit()
  return redirect(url_for("admin.messages"))
  
  
@admin.route("/messages/archive")
@login_required
def archive():
  messages=Contact.query.order_by(Contact.id.desc()).all()
  for message in messages:
    read=message.is_read()
  return render_template("archive.html", messages=messages, read=read)

  
@admin.route("/message/<int:id>/delete")
@login_required
def delete_message(id):
  message=Contact.query.get_or_404(id)
  db.session.delete(message)
  db.session.commit()
  return redirect(url_for("admin.archive"))
  
