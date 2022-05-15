from random import randrange 
from sqlite3 import Connection as SQLite3Connection 
from datetime import datetime 
from faker import Faker 
from sqlalchemy.engine import Engine 
from sqlalchemy import event 
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
#import otherexample 
#from models import User, Post, Comment, PostCategory
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__) 

app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///Blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapl_connection, connection_record):
  if isinstance(dbapl_connection, SQLite3Connection):
    cursor = dbapl_connection.cursor()
    cursor.execute("PRAGMA ForeignKeys=ON;")
    cursor.close()
    
db = SQLAlchemy(app)
now = datetime.now()

faker = Faker()

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)  
  first_name = db.Column(db.String(20), nullable=False)
  last_name = db.Column(db.String(20), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(50), nullable=False)
  image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
  admin = db.Column(db.Boolean(), default=False)
  posts = db.relationship("Post", backref="author", lazy=True, cascade="all, delete")
  executive = db.relationship("Executives", backref="exco", lazy=True, cascade="all, delete")
  reset_codes = db.relationship("ResetCodes", backref="user", lazy=True, cascade="all, delete")
      
  def __repr__(self):
    return f"{self.first_name} {self.last_name}"
 
  def verify_password(self, password):
    return check_password_hash(self.password, password)
    
  def is_admin(self):
    return self.admin

    
class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  date_posted = db.Column(db.DateTime(120), nullable=False, default=datetime.utcnow)
  image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
  content = db.Column(db.Text, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
  comment = db.relationship("Comment", backref="post", lazy=True, cascade="all, delete")
  category = db.relationship("PostCategory", backref="post", lazy=True, cascade="all, delete")
  
  def __repr__(self):
    return f"Posts {self.title}, {self.date_posted}"
    
    
class Comment(db.Model):
  id = db.Column(db.Integer, primary_key=True) 
  name = db.Column(db.String(30), nullable=False)
  email = db.Column(db.String(120), nullable=False)
  comment = db.Column(db.String(250), nullable=False)
  post_id = db.Column(db.ForeignKey("post.id"), nullable=False)
  comment_date = db.Column(db.DateTime(120), nullable=False, default=datetime.utcnow)
  
  def __repr__(self):
    return f"{self.comment}"
    
  
class Executives(db.Model):
  id = db.Column(db.Integer, primary_key=True) 
  user_id = db.Column(db.ForeignKey("user.id"), nullable=False)
  post = db.Column(db.String(50), nullable=False)
  promotion_date = db.Column(db.DateTime(120), nullable=False, default=datetime.utcnow)
  
  
class Category(db.Model):
  id = db.Column(db.Integer, primary_key=True) 
  name = db.Column(db.String(25), nullable=False)
  category = db.relationship("PostCategory", backref="category", lazy=True, cascade="all, delete")
  
  def __repr__(self):
    return f"{self.name}"
  
  
class PostCategory(db.Model):
  id = db.Column(db.Integer, primary_key=True) 
  post_id = db.Column(db.ForeignKey("post.id"), nullable=False)
  cat_id = db.Column(db.ForeignKey("category.id"), nullable=False)


# ("Web development", "Artswork", "Design", "Creative", "Video", "Audio", "Visual", "Music", "Business", "Travel", "Events")

class Contact(db.Model):
  id = db.Column(db.Integer, primary_key=True) 
  name = db.Column(db.String(50), nullable=False)
  email = db.Column(db.String(120), nullable=False)
  subject = db.Column(db.String(25), nullable=False)
  message = db.Column(db.String(250), nullable=False)
  date = db.Column(db.DateTime(120), nullable=False, default=datetime.utcnow)
  read = db.Column(db.Boolean(), default=False)
  
  
  def is_not_read(self):
    return not self.read
  
  
class ResetCodes(db.Model):
  id = db.Column(db.Integer, primary_key=True) 
  user_id = db.Column(db.Integer, db.ForeignKey(User.id))
  code = db.Column(db.Integer, nullable=False)
  timestamp = db.Column(db.DateTime(120), nullable=False, default=datetime.utcnow())
  used = db.Column(db.Boolean(), nullable=False, default=False)
  
  def is_used(self):
    return self.used
    
  def code_status(self, code, user):
    expiring_time = datetime.timedelta(seconds=30)
    now = datetime.datetime.utcnow()
    
    if self.user==user and self.code!=code and self.timestamp + expiring_time > now:
      return "Invalid"
    elif self.user==user and self.code==code and self.timestamp + expiring_time < now:
      return "Expired"
    elif self.user==user and self.code==code and self.timestamp + expiring_time > now and self.used==False:
      return "Valid"
      
  def mark_used(self):
    self.used=True


# # creating dummy users
# for l in range(10):
#   last_name = faker.last_name()
#   first_name = faker.first_name()
#   email = f"{first_name}.{last_name}@email.com"
#   password = generate_password_hash("goodluck")
#   new_user = User(last_name=last_name, first_name=first_name, email=email, password=password,)
#   db.session.add(new_user)
#   db.session.commit()
  
# # creating dummy post
# for l in range(100):
#   title = faker.sentence(3)
#   user_id = randrange(1, 10)
#   content = faker.paragraph(10)
#   post = Post(title=title, content=content, user_id=user_id)
#   db.session.add(post)
#   db.session.commit()
  
# # creating dummy comments
# for l in range(500):
#   name = faker.name()
#   email = f"{name.replace('', '_')}.email.com"
#   comment = faker.sentence()
#   post_id = randrange(1, 100)
#   com = Comment(name=name, post_id=post_id, comment=comment, email=email)
#   db.session.add(com)
#   db.session.commit()
  
# creating dummy postcategory
post_id = 1
while True:
  if post_id > 100:
    break
  for l in range(3):
    cat_id=randrange(1, 10)
    postcat = PostCategory(post_id=post_id, cat_id=cat_id)
    db.session.add(postcat)
    db.session.commit()
    post_id += 1