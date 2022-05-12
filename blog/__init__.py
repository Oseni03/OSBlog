from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from flask_mail import Mail
from flask_mail import Message

app = Flask(__name__)

login_manager = LoginManager(app)
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"

app.config['UPLOAD_FOLDER'] = os.path.realpath('.') + '/blog/static/img'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Blog.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '9ab803b32301726f09247060e35175'
db = SQLAlchemy(app)

# After 'Create app'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'officialcontact788@gmail.com'
app.config['MAIL_PASSWORD'] = 'ysnxhvlbzjpdynve'
mail = Mail(app)

app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[OSBlog]'
app.config['FLASKY_MAIL_SENDER'] = 'OSBlog Admin <officialcontact788@gmail.com>'


from blog.admin.admin import admin
from blog.auth.auth import auth
from blog.post.post import post
from blog.user.user import user

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(post, url_prefix='/post')
app.register_blueprint(user, url_prefix='/user')



