from datetime import datetime
from blog import db, login_manager, app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from itsdangerous.serializer import Serializer


@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(20), nullable=False)
  last_name = db.Column(db.String(20), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(50), nullable=False)
  image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
  admin = db.Column(db.Boolean(), default=False)
  posts = db.relationship("Post", backref="author", lazy=True, cascade="all, delete")
  executive = db.relationship("Executives", backref="exco", lazy=True, cascade="all, delete")
      
  def __repr__(self):
    return f"{self.first_name} {self.last_name}"
 
  def verify_password(self, password):
    return check_password_hash(self.password, password)
    
  def is_admin(self):
    return self.admin
    
    
  def get_reset_token(self, expires_sec=1800):
    s= Serializer(app.config["SECRET_KEY"])
    return s.dumps({"user_id": self.id})
    
    
  def verify_reset_token(token):
    s= Serializer(app.config["SECRET_KEY"])
    try:
      user_id = s.loads(token)["user_id"]
    except:
      return None
    return user_id

    
class Post(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  date_posted = db.Column(db.DateTime(120), nullable=False, default=datetime.datetime.utcnow)
  image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
  content = db.Column(db.Text, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
  comment = db.relationship("Comment", backref="post", lazy=True, cascade="all, delete")
  category = db.relationship("PostCategory", backref="post", lazy=True, cascade="all, delete")
  
  def __repr__(self):
    return f"Posts {self.title}, {self.date_posted}"
    
    
class Comment(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True) 
  name = db.Column(db.String(30), nullable=False)
  email = db.Column(db.String(120), nullable=False)
  comment = db.Column(db.String(250), nullable=False)
  post_id = db.Column(db.ForeignKey("post.id"), nullable=False)
  comment_date = db.Column(db.DateTime(120), nullable=False, default=datetime.datetime.utcnow)
  
  def __repr__(self):
    return f"{self.comment}"
    
  
class Executives(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True) 
  user_id = db.Column(db.ForeignKey("user.id"), nullable=False)
  post = db.Column(db.String(50), nullable=False)
  promotion_date = db.Column(db.DateTime(120), nullable=False, default=datetime.datetime.utcnow)
  
  
class Category(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True) 
  name = db.Column(db.String(25), nullable=False)
  category = db.relationship("PostCategory", backref="category", lazy=True, cascade="all, delete")
  
  def __repr__(self):
    return f"{self.name}"
  
  
class PostCategory(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True) 
  post_id = db.Column(db.ForeignKey("post.id"), nullable=False)
  cat_id = db.Column(db.ForeignKey("category.id"), nullable=False)
  
  def __init__(self, post_id, category):
    self.post_id=post_id
    self.category=category

# ("Web development", "Artswork", "Design", "Creative", "Video", "Audio", "Visual", "Music", "Business", "Travel", "Events")

class Contact(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True) 
  name = db.Column(db.String(50), nullable=False)
  email = db.Column(db.String(120), nullable=False)
  subject = db.Column(db.String(25), nullable=False)
  message = db.Column(db.String(250), nullable=False)
  date = db.Column(db.DateTime(120), nullable=False, default=datetime.datetime.utcnow)
  read = db.Column(db.Boolean(), default=False)
  
  def is_read(self):
    return self.read
  
  def is_not_read(self):
    return not self.read
  
  
