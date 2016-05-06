from flask import Flask
from debmetrics.config_reader import settings, read_config
import os

from debmetrics.database import db

pkg_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder=os.path.join(pkg_dir, '..', 'static'),
            template_folder=os.path.join(pkg_dir, '..', 'templates'))

read_config()

app.config['SECRET_KEY'] = settings['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = settings['DB_URI']
db.init_app(app)
