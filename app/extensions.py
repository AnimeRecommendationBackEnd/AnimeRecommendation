from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
import redis


db = SQLAlchemy()
r = redis.Redis()

def login_required(func):
    def yes_or_no():
        if r.get('user') is None:
            return jsonify({'error':'no login'})
        return func()
    return yes_or_no
