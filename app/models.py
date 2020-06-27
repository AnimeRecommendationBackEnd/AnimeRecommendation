from app.extensions import db
from passlib.apps import custom_app_context as pwd_context


#users数据表,用户名以及邮箱唯一
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),unique=True)
    password = db.Column(db.String(20))
    avatar = db.Column(db.String(50))
    email = db.Column(db.String(20),unique=True)

    #以用户名进行加密
    def make_token(self):
        return pwd_context.encrypt(self.name)

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    password = db.Column(db.String(20))
