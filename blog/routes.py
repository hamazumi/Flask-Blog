from flask import render_template, url_for, redirect, request
from blog import app, db
from blog.forms import RegistrationForm, LoginForm
from blog.models import User, Post
from flask_login import login_user, logout_user, current_user

posts = [
    {
        'author': 'KEN test',
        'title': 'TEST Post 1',
        'content': 'TEST content 1',
        'date_posted': 'July 26, 2021'
    },
    {
        'author': 'JESS test',
        'title': 'TEST Post 2',
        'content': 'TEST content 2',
        'date_posted': 'July 26, 2021'
    },
    {
        'author': 'BUDDHA test',
        'title': 'TEST Post 3',
        'content': 'TEST content 3',
        'date_posted': 'July 26, 2021'
    }
]

# APP ROUTES
@app.route('/')
@app.route('/home')
def homepage():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        # check for matching email
        user = User.query.filter_by(email = form.email.data).first()
        password = form.password.data
        if user and password:
            login_user(user, remember = form.remember.data)
            return redirect(url_for('homepage'))
    return render_template('login.html', title='Login', form=form)
    

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))
