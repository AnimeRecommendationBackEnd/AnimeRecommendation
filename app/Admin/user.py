from app.extensions import *
from app.models import *
from app.Admin import admin


def deleteToken(userId):
    keys = r.keys()
    target = ''
    for key in keys:
        # print(str(r.get(key), encoding='utf8'), str(userId))
        if str(r.get(key), encoding='utf8') == str(userId):
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

