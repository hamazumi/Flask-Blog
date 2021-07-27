from datetime import datetime
from blog import db, login_manager
from flask_login import UserMixin

# --------------CHECKS TO SEE LOGGED IN USER BY ID-----------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------------USER MODEL FOR DATABASE----------------
class User(db.Model, UserMixin):
# ----------------SETTING UP COLUMNS FOR DATABASE--------------
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

# ---------------SET UP HOW INFO IS SHOWN WHEN YOU USE TERMINAL--------------
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# ------------------POST MODEL FOR DATABASE----------------
class Post(db.Model):
# ----------------SETTING UP COLUMNS FOR DATABASE--------------
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# ---------------SET UP HOW INFO IS SHOWN WHEN YOU USE TERMINAL--------------
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
