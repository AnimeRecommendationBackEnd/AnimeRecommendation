from datetime import datetime

from passlib.apps import custom_app_context as pwd_context

from app.extensions import db,whooshee


# cascade='all'为当前表删除时，有cascade='all'的外键表也一同删除

class Follow(db.Model):
    __tablename__ = "follow"
    followerid = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    followedid = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

# users数据表,用户名以及邮箱唯一
@whooshee.register_model('name')
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    followed = db.relationship('Follow',foreign_keys=[Follow.followerid],
                               backref=db.backref('follower',lazy='joined'),        #粉丝
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    follower = db.relationship('Follow',foreign_keys=[Follow.followedid],
                                backref=db.backref('followed',lazy='joined'),           #关注
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    name = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    avatar = db.Column(db.String(100))
    email = db.Column(db.String(20), unique=True)
    dramas = db.relationship('Drama', back_populates='user', cascade='all')
    likes = db.relationship('Likedrama', back_populates='user', cascade='all')  # 点赞
    collects = db.relationship('Collectdrama', back_populates='user', cascade='all')  # 收藏
    animecomments = db.relationship('AnimeComment', backref='user')
    animelikes = db.relationship('AnimeLike', backref='user')
    animecommentstars = db.relationship('AnimeCommentStar', backref='user')

    # 以用户名进行加密
    def make_token(self):
        return pwd_context.encrypt(self.name)



# 点赞表
class Likedrama(db.Model):
    __tablename__ = "likedrama"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='likes')
    drama_id = db.Column(db.Integer, db.ForeignKey('drama.id'))
    drama = db.relationship('Drama', back_populates='likes')
    follow = db.Column(db.Boolean,default=False)


# 收藏表
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


# 推荐表（问番表）
@whooshee.register_model('title')
class Drama(db.Model):
    __tablename__ = "drama"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))  # 标题
    content = db.Column(db.Text)  # 内容
    time = db.Column(db.DateTime, default=datetime.utcnow, index=True)  # 时间
    likes = db.relationship('Likedrama', back_populates='drama')  # 点赞
    collects = db.relationship('Collectdrama', back_populates='drama')  # 收藏
    photos = db.relationship('Photo', back_populates='drama', cascade='all')  # 图片包含封面图片和内容图片，会有标志区分
    comments = db.relationship('Comment', back_populates='drama', cascade='all')  # 评论
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='dramas')  # 发布人
    top = db.Column(db.Integer)  # 置顶的评论id
    anime = db.relationship('Anime',back_populates='drama')
    solution = db.Column(db.String(10), default=None)  # 问番的解决状态


# 图片表
class Photo(db.Model):
    __tablename__ = "photo"
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(100))  # 图片文件名
    drama_id = db.Column(db.Integer, db.ForeignKey('drama.id'))
    drama = db.relationship('Drama', back_populates='photos')
    cover = db.Column(db.Boolean, default=False)  # 封面图片，是就改为True
    content = db.Column(db.Boolean, default=False)  # 内容图片，是就改为True


# 评论表，因为参照B站用户被注销评论还在所以就没有连接用户表
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)  # 内容
    time = db.Column(db.DateTime,default=datetime.utcnow,index=True)
    author_id = db.Column(db.Integer)  # 评论人id
    author = db.Column(db.String(20))  # 评论人名
    email = db.Column(db.String(20))
    drama_id = db.Column(db.Integer, db.ForeignKey('drama.id'))
    drama = db.relationship('Drama', back_populates='comments')  # 所在推荐表


class Anime(db.Model):
    __tablename__ = 'anime'
    id = db.Column(db.Integer, primary_key=True)
    seasonId = db.Column(db.String(50))
    mediaId = db.Column(db.String(50))
    picture = db.Column(db.String(100))
    title = db.Column(db.String(100))
    describe = db.Column(db.Text)
    isShow = db.Column(db.Boolean, default=False)
    link = db.Column(db.String(100))
    isFinish = db.Column(db.Boolean)
    # tag标签代码在utils里
    tag1 = db.Column(db.String(10))
    tag2 = db.Column(db.String(10))
    tag3 = db.Column(db.String(10))
    # 数据来源：
    # 1：bilibili
    # 2：用户推荐
    datafrom = db.Column(db.Integer)
    comments = db.relationship('AnimeComment', backref='anime')
    likes = db.relationship('AnimeLike', backref='anime')
    likenum = db.Column(db.Integer, default=0)
    dramaid = db.Column(db.Integer,db.ForeignKey('drama.id'))
    drama = db.relationship('Drama',back_populates='anime')


class AnimeComment(db.Model):
    __tablename__ = 'animecomment'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    animeId = db.Column(db.Integer, db.ForeignKey('anime.id'))
    comment = db.Column(db.TEXT)
    # time = db.Column(db.DateTime, default=datetime.utcnow)
    stars = db.relationship("AnimeCommentStar", backref='animecomment')
    starnum = db.Column(db.Integer, default=0)


class AnimeLike(db.Model):
    __tablename__ = 'animelike'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    animeId = db.Column(db.Integer, db.ForeignKey('anime.id'))


class AnimeCommentStar(db.Model):
    __tablename__ = 'animecommentstar'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    animeCommentId = db.Column(db.Integer, db.ForeignKey('animecomment.id'))


class AnimeLog(db.Model):
    __tablename__ = 'adminlog'
    id = db.Column(db.Integer, primary_key=True)
    opreate = db.Column(db.TEXT)
    time = db.Column(db.DateTime, default=datetime.utcnow)


