from flask import Flask, render_template, url_for, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'TOPSECRET'

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
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect(url_for('homepage'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            return redirect(url_for('homepage'))
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)