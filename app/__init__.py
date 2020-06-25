from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('settings.py')

db = SQLAlchemy(app)

from app.Anime import anime
from app.User import user

app.register_blueprint(anime, url_prefix='/anime')
app.register_blueprint(user, url_prefix='/user')
