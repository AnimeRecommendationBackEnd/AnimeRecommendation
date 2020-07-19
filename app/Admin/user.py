from app.extensions import *
from app.models import *
from app.Admin import admin


def deleteToken(userId):
    keys = r.keys()
    for key in keys:
        getId = str(r.get(key), encoding='utf8')
        if getId == str(userId) and len(getId) != 32:
            r.delete(key)


# 用户封号接口
# 发邮件提醒
@admin.route("/userlock", methods=['POST'])
@admin_login
def userLock(token):
    adminId = r.get(token)
    admin = Admin.query.get(adminId)
    userId = request.form.get('userid')
    user = User.query.get(userId)
    # 删除token, 用户状态改为封号
    deleteToken(userId)
    user.status = False
    db.session.commit()
    # 发邮件
    send_email('警告', user.email, '您的账号被封禁')
    return jsonify(Event0(token=token))

# 用户解封接口
# 发邮件提醒
@admin.route("/userunlock", methods=['POST'])
@admin_login
def userUnLock(token):
    adminId = r.get(token)
    admin = Admin.query.get(adminId)
    userId = request.form.get('userid')
    user = User.query.get(userId)
    # 用户状态改为解封
    user.status = True
    db.session.commit()
    # 发邮件
    send_email('警告', user.email, '您的账号已解禁')
    return jsonify(Event0(token=token))


# 获取用户信息
# 发布的问番，荐番，评论
@admin.route('/getuser', methods=['POST'])
@admin_login
def getUser(token):
    adminId = r.get(token)
    admin = Admin.query.get(adminId)
    userId = request.form.get('userid')
    user = User.query.get(userId)
    comments = Comment.query.filter_by(author_id=userId)
    animecomments = AnimeComment.query.filter_by(userId=userId)
    commentlist = []
    animecommentlist = []
    for comment in comments:
        temp = {
            "commentid": comment.id,
            "dramatitle": comment.drama.title,
            "dramaid": comment.drama.id,
            "authorname": comment.author,
            "authorid": comment.author_id,
            "content": comment.text,
            "time": comment.time
        }
        commentlist.append(temp)
    for animecomment in animecomments:
        temp = {
            "commentid": animecomment.id,
            "animetitle": animecomment.anime.title,
            "animeid": animecomment.anime.id,
            "authorname": animecomment.author,
            "authorid": animecomment.author_id,
            "content": animecomment.text,
            "time": animecomment.time
        }
        animecommentlist.append(temp)
    data = Giveuser(user)
    data['comments'] = commentlist
    data['animecomments'] = animecommentlist
    return jsonify(
        {
            "status": 0,
            "data": data
        }
    )

