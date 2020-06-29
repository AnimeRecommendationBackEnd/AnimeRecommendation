from flask import Flask
from app.extensions import *
from app.models import User,Admin
from app.Anime import anime
from app.User import user
from app.Admin import admin
import click


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')

    register_extensions(app)
    register_blueprint(app)
    register_command(app)

    return app

def register_extensions(app):
    db.init_app(app)
    mail.init_app(app)


def register_blueprint(app):
    app.register_blueprint(anime, url_prefix='/anime')
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(admin, url_prefix='/admin')


def register_command(app):

    @app.cli.command()
    def initdb():
        db.drop_all()
        db.create_all()
        click.echo('create success')

    @app.cli.command()
    def addadmin():
        admin1 = Admin(name='admin', password='admin')
        try:
            db.session.add(admin1)
            db.session.commit()
            click.echo('add success')
        except:
            click.echo('add fail')

