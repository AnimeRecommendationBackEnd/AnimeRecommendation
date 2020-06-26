from flask import Flask
# from app.extensions import *
from app.models import *
from app.Anime import anime
from app.User import user
import click


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')

    register_blueprint(app)
    register_command(app)
    register_extensions(app)
    register_command(app)

    return app

def register_extensions(app):
    db.init_app(app)


def register_blueprint(app):
    app.register_blueprint(anime, url_prefix='/anime')
    app.register_blueprint(user, url_prefix='/user')


def register_command(app):

    @app.cli.command()
    def initdb():
        db.drop_all()
        db.create_all()
        click.echo('create success')

