from debmetrics.app import app
from debmetrics.database import db
from debmetrics.models.user import User

print('Create a new user.\n')

username = input('Enter a username: ')
password = input('Enter a password: ')

user = User(username, password)

with app.app_context():
    db.session.add(user)
    db.session.commit()
