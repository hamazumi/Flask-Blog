To run SQLAlchemy:

$ python3
$ from __name of app(blog)____ import db
$ from blog.models import User
$ User.query.all()   shows all users

delete a user
$ User.query.filter_by(id=123).delete()