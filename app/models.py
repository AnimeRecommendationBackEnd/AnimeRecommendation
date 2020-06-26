from app.extensions import db


#users数据表
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    password = db.Column(db.String(20))
    avatar = db.Column(db.String(50))
    email = db.Column(db.String(20))

