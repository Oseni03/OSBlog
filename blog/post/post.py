import secrets, os
from flask import render_template, redirect, url_for, flash, abort, Blueprint, request, current_app
from blog import app, db 
from PIL import Image
from blog.models import User, Post, Category, PostCategory, Comment
from blog.post.forms import CommentForm, CreatePostForm
from flask_login import login_user, current_user, logout_user, login_required
from blog.auth.forms import SearchForm


post = Blueprint('post', __name__,
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
  
  #filename.save(os.path.join(app.config['UPLOAD_FOLDER'], picture_fn))
  return picture_fn
  
  
@post.route("/post/<int:post_id>", methods=["GET", "POST"])
def single_post(post_id):
  post=Post.query.get_or_404(post_id)
  comments=Comment.query.filter_by(post=post).order_by(Comment.comment_date.desc()).limit(3)
  user=None
  for comment in comments:
    user = User.query.filter_by(email=comment.email).first()
  categories=Category.query.all()
  
  # TO FIND ALL THE POSTCATEGORIES IDS ASSOCIATED WITH THE POST 
  rel_id=[]
  for rel in post.category:
    rel_id.append(rel.cat_id)
    
  
  # TO FIND ALL THE CATEGORIES IDS ASSOCIATED WITH THE POSTCATEGORY  
  cats=[]
  for id in rel_id:
    cats.append(PostCategory.query.filter_by(cat_id=id).limit(5).all())
    
  categorys=[]
  for cat in cats:
    for c in cat:
      categorys.append(c)
      
  # TO FIND POSTS ASSOCIATED WITH EACH CATEGORY IN THE LIST
  rel_posts=[]
  for category in categorys:
    if category.post not in rel_posts:
      rel_posts.append(category.post)
      if len(rel_posts) == 3:
        break
  
  
  form=CommentForm()
  if form.validate_on_submit():
    comment = Comment(name=form.name.data, email=form.email.data, post=post, comment=form.comment.data)
    db.session.add(comment)
    db.session.commit()
    flash("Comment successful", "success")
    return redirect(url_for("post.single_post", post_id=post.id))
  
  return render_template("post.html", post=post, categories=categories, comments=comments, user=user, form=form, rel_posts=rel_posts)
  
  
@post.route("/create_post", methods=["GET", "POST"])
@login_required
def create_post():
  form=CreatePostForm()
  pic=""
  if form.is_submitted():
    picture=form.picture.data
    try:
      pic = secure_filename(picture)
    except:
      flash("Not supported image format", "warning")
    if pic:
      post = Post(
        title = form.title.data,
        content = form.content.data,
        image_file = pic,
        author = current_user
        )
      db.session.add(post)
      db.session.flush()
      categories=form.category.data
      for category in categories:
        cat = Category.query.get(category)
        new_cat=PostCategory(post.id, cat)
        db.session.add(new_cat)
        db.session.commit()
      db.session.commit()
        
      flash("Post created successfully", "success")
      return redirect(url_for("auth.home"))
    else:
      categories=form.category.data
      post = Post(
        title = form.title.data,
        content = form.content.data,
        author = current_user
        )
      db.session.add(post)
      db.session.flush()
      for category in categories:
        cat = Category.query.get(category)
        new_cat=PostCategory(post.id, cat)
        db.session.add(new_cat)
        db.session.commit()
      db.session.commit()
        
      flash("Post created successfully", "success")
      return redirect(url_for("auth.home"))
  return render_template("create_post.html", form=form, title="Create Post", legend="Create Post")
  
  
@post.route("/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def post_update(post_id):
  post = Post.query.get_or_404(post_id)
  postcats = PostCategory.query.filter_by(post=post).all()
  if post.author != current_user:
    abort(403)
  form = CreatePostForm()
  if form.validate_on_submit():
    picture=form.picture.data
    pic=""
    if picture:
      pic = secure_filename(picture)
      picture.save(os.path.join(app.config['UPLOAD_FOLDER'], pic))
      post.image_file = str(pic),
      db.session.commit()
    post.title = str(form.title.data)
    post.content = str(form.content.data)
    db.session.commit()

    flash("Post updated successfully", "success")
    return redirect(url_for("post.single_post", post_id=post_id))
  elif request.method == "GET":
    form.title.data = post.title
    form.content.data = post.content
    form.picture.data=post.image_file
  return render_template("update_post.html", title="Update Post", form=form, legend="Update Post", post=post)
  
  
@post.route("/post/<int:post_id>/delete", methods=["POST", "GET"])
@login_required
def delete_post(post_id):
  post = Post.query.get_or_404(post_id)
  if post.author != current_user:
    abort(403)
  db.session.delete(post)
  db.session.commit()
  flash("Post deleted successfully", "success")
  return redirect(url_for("auth.home"))
  
  
@post.route("/category/<int:cat_id>/posts", methods=["POST", "GET"])
def cat_posts(cat_id):
  page = request.args.get("page", 1, type=int)
  form=SearchForm()
  #postcats = PostCategory.query.filter_by(cat_id=cat_id).all()
  cat = Category.query.get(cat_id)
  postcats = PostCategory.query.filter(PostCategory.category==cat).paginate(page=page, per_page=15)
  posts = []
  for postcat in postcats.items:
    posts.append(postcat.post)
  if form.validate_on_submit():
    search_word=form.search.data
    if search_word:
      posts=Post.query.filter(Post.title.like("%" + search_word + "%")).all().paginate(page=page, per_page=15)
  return render_template("cat_posts.html", posts=posts, form=form, title="Category Post", paging=postcats, cat_id=cat_id)