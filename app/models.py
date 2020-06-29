from app.extensions import db
from datetime import datetime
from passlib.apps import custom_app_context as pwd_context

#cascade='all'为当前表删除时，有cascade='all'的外键表也一同删除

#users数据表,用户名以及邮箱唯一
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),unique=True)
    password = db.Column(db.String(20))
    avatar = db.Column(db.String(50))
    email = db.Column(db.String(20),unique=True)
    dramas = db.relationship('Drama',back_populates='user',cascade='all')
    follow_id = db.Column(db.Integer,db.ForeignKey('user.id'))          #关注实现，邻接列表关系
    follows = db.relationship('User',back_populates='follow',remote_side=[id])
    follow = db.relationship('User',back_populates='follows',cascade='all')
    likes = db.relationship('Likedrama',back_populates='user',cascade='all')        #点赞
    collects = db.relationship('Collectdrama',back_populates='user',cascade='all')      #收藏

    #以用户名进行加密
    def make_token(self):
        return pwd_context.encrypt(self.name)

#点赞表
class Likedrama(db.Model):
    __tablename__ = "likedrama"
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    user = db.relationship('User',back_populates='likes')
    drama_id = db.Column(db.Integer, db.ForeignKey('drama.id'))
    drama = db.relationship('Drama',back_populates='likes')

#收藏表
class Collectdrama(db.Model):
    __tablename__ = "collectdrama"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='collects')
    drama_id = db.Column(db.Integer, db.ForeignKey('drama.id'))
    drama = db.relationship('Drama', back_populates='collects')

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    password = db.Column(db.String(20))


#推荐表（问番表）
class Drama(db.Model):
    __tablename__ = "drama"
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(20))    #标题
    content = db.Column(db.Text)    #内容
    time = db.Column(db.DateTime,default=datetime.utcnow,index=True)        #时间
    likes = db.relationship('Likedrama',back_populates='drama')         #点赞
    collects = db.relationship('Collectdrama',back_populates='drama')       #收藏
    photos = db.relationship('Photo',back_populates='drama',cascade='all')  #图片包含封面图片和内容图片，会有标志区分
    comments = db.relationship('Comment',back_populates='drama',cascade='all')  #评论
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    user = db.relationship('User',back_populates='dramas')      #发布人
    top = db.Column(db.Integer)         #置顶的评论id
    synopsis = db.Column(db.String(100))        #简介
    bvid = db.Column(db.String(10))
    web = db.Column(db.String(30))
    solution = db.Column(db.String(10),default=None)        #问番的解决状态

#图片表
class Photo(db.Model):
    __tablename__ = "photo"
    id = db.Column(db.Integer,primary_key=True)
    image = db.Column(db.String(50))        #图片文件名
    drama_id = db.Column(db.Integer,db.ForeignKey('drama.id'))
    drama = db.relationship('Drama',back_populates='photos')
    cover = db.Column(db.Boolean,default=False)     #封面图片，是就改为True
    content = db.Column(db.Boolean,default=False)       #内容图片，是就改为True

#评论表，因为参照B站用户被注销评论还在所以就没有连接用户表
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)   #内容
    author_id = db.Column(db.Integer)   #评论人id
    author = db.Column(db.String(20))   #评论人名
    drama_id = db.Column(db.Integer,db.ForeignKey('drama.id'))
    drama = db.relationship('Drama',back_populates='comments')      #所在推荐表



class finishedAnime(db.Model):
    __tablename__ = 'finishedanime'
    id = db.Column(db.Integer, primary_key=True)
    bvid = db.Column(db.String(50))
    picture = db.Column(db.String(100))
    title = db.Column(db.String(100))
    introduce = db.Column(db.Text)
    createtime = db.Column(db.String(20))
    isShow = db.Column(db.Boolean, default=True)
