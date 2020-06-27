from flask import jsonify,request
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask_mail import Mail,Message
import redis


db = SQLAlchemy()
mail = Mail()
r = redis.Redis()

#登录验证装饰器
def login_required(func):
    @wraps(func)
    def yes_or_no():
        token = request.form.get('token')
        if r.get(token) is None:
            return jsonify({'error':'no login'})
        return func(token)
    return yes_or_no


#发送邮件函数
def send_email(subject,to,body):
    message = Message(subject=subject,recipients=[to],body=body)
    mail.send(message)
