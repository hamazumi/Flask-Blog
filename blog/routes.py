from flask import render_template, url_for, redirect, request, abort
from blog import app, db
from blog.forms import RegistrationForm, LoginForm, PostForm
from blog.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required


# ------------------APP ROUTES BELOW!!!-----------------

@app.route('/')
@app.route('/home')
def homepage():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

# ------------------ABOUT PAGE-----------------
@app.route('/about')
def about():
    return render_template('about.html', title='About')

# ------------------REGISTER PAGE-----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    # -----------IF CURRENT USER LOGGED IN REDIRECTED TO HOMEPAGE------------
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = RegistrationForm()
    # -----------IF FORM VALIDATED, ADD USER TO DATABASE AND REDIRECT TO LOGIN------------
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# ------------------LOGIN PAGE-----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
     # -----------IF CURRENT USER LOGGED IN REDIRECTED TO HOMEPAGE------------
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    # -----------IF FORM VALIDATED, COMPARE WITH DB EMAIL/PASSWORD THEN REDIRECT TO HOMEPAGE------------
    if form.validate_on_submit():
        # check for matching EMAIL
        user = User.query.filter_by(email = form.email.data).first()
         # check for matching PASSWORD
        password = form.password.data
        if user and password:
            login_user(user, remember = form.remember.data)
            return redirect(url_for('homepage'))
    return render_template('login.html', title='Login', form=form)

# ------------------LOGOUT ROUTE-----------------
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))

# ------------------NEW POST FORM PAGE-----------------
@app.route('/post/new', methods = ['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('homepage'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

# ------------------SINGLE POST PAGE-----------------
@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

# ------------------EDIT SINGLE POST PAGE-----------------
@app.route('/post/<int:post_id>/update', methods = ['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        # No need to db add because you are updating db
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        return redirect(url_for('post', post_id=post.id))
    # Below fills out form with current data
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Edit Post', form=form, legend='Edit Post')

# ------------------DELETE-----------------
@app.route('/post/<int:post_id>/delete', methods = ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('homepage'))