from flask import jsonify,request,session, redirect, url_for,current_app
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_whooshee import Whooshee
from functools import wraps
from flask_mail import Mail,Message
from threading import Thread
import redis

db = SQLAlchemy()
mail = Mail()
whooshee = Whooshee()
r = redis.Redis()
migrate = Migrate()

from app.models import Photo,Drama

#登录验证装饰器
def login_required(func):
    @wraps(func)
    def yes_or_no():
        token = request.form.get('token')
        if r.get(token) is None:
            return jsonify(Event1001())
        return func(token)
    return yes_or_no

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

def admin_login(func):
    @wraps(func)
    def yes_or_no():
        token = request.form.get('token')
        if r.get(token) is None:
            return jsonify(Event1001())
        return func(token)
    return yes_or_no


#发送邮件函数
def send_email(subject,to,body):
    app = current_app._get_current_object()
    message = Message(subject=subject,recipients=[to],body=body)
    thr = Thread(target=send_async_email,args=[app,message])
    thr.start()
    return thr


def Event0(**kwargs):
    return {
                "status": 0,
                "data": kwargs
            }

def Event1001():
    return {
            "status": 1001,
            "message": "token失效"
        }

def Event1002():
    return {
            "status": 1002,
            "message": "对象不存在"
        }

def Event1003():
    return {
            "status": 1003,
            "message": "已存在对象"
        }

def Event1004():
    return {
            "status": 1004,
            "message": "请求错误"
        }

def Event1005(message):
    return {
                "status": 1005,
                "message": message
            }

def Giveuser(user):
    Rdramas = Drama.query.filter(Drama.user_id==user.id,Drama.solution==None).all()
    Adramas = Drama.query.filter(Drama.user_id==user.id,Drama.solution!=None).all()

    return {
        "userid": user.id,
        "name": user.name,
        "avatar": user.avatar,
        "email": user.email,
        "Rdramas": len(Rdramas),
        "Adramas": len(Adramas),
        "collects": len(user.collects),
        "fans": len(user.followed.all()),
        'followers':len(user.follower.all())
    }


def Givedrama(drama):
    photos = Photo.query.filter_by(drama_id=drama.id,content=True).all()
    animepictures = Photo.query.filter_by(drama_id=drama.id,cover=True).all()
    if drama.anime[0].datafrom == 1:
        animelink = drama.anime[0].seasonId
    else:
        animelink = drama.anime[0].link

    return {
            "dramaid": drama.id,
            "authorid": drama.user.id,
            "authorname": drama.user.name,
            "title": drama.title,
            "content": drama.content,
            "time": drama.time,
            "photos": [photo.image for photo in photos],
            "animetitle": drama.anime[0].title,
            "animedescribe": drama.anime[0].describe,
            "animepicture": [photo.image for photo in animepictures],
            "animefrom": drama.anime[0].datafrom,
            "animelink": animelink,
            "tag": [ [{"tag1":anime.tag1},{"tag2":anime.tag2},{"tag3":anime.tag3}] for anime in drama.anime],
            "comment": [Givecomment(comment) for comment in drama.comments]
        }

def Givecomment(comment):
    return {
                "commentid": comment.id,
                "authorname": comment.author,
                "authorid": comment.author_id,
                "content": comment.text,
                "time": comment.time
            }

def Giveask(drama):
    photos = Photo.query.filter_by(drama_id=drama.id, content=True).all()
    return {
        "dramaid": drama.id,
        "authorid": drama.user.id,
        "authorname": drama.user.name,
        "title": drama.title,
        "content": drama.content,
        "time": drama.time,
        "photos": [photo.image for photo in photos],
        "comment": [Givecomment(comment) for comment in drama.comments]
    }

def Giveperson(user):
    return {
        'userid':user.id,
        'name':user.name,
        'avatar':user.avatar,
        'email':user.email,
        "fans": len(user.followed.all()),
        'followers': len(user.follower.all())
    }


def Givep_recommentd(drama):
    photos = Photo.query.filter_by(drama_id=drama.id, cover=True).all()
    return {
        'dramaid': drama.id,
        'title': drama.title,
        'photo': [photo.image for photo in photos]
    }

def Givep_ask(drama):
    photos = Photo.query.filter_by(drama_id=drama.id, content=True).all()
    return {
        'dramaid': drama.id,
        'title': drama.title,
        'photo': [photo.image for photo in photos]
    }