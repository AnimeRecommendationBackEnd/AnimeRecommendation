from app.Admin import admin
from app.extensions import *
from app.models import *


@admin.route('/login', methods=['POST'])
def adminLogin():
    name = request.form.get('name')
    password = request.form.get('password')

    admin = Admin.query.filter_by(name=name).first()
    if admin is None:
        return jsonify(Event1002())
    token = admin.makeToken()
    r.set(token, str(admin.id))
    if admin.checkPwd(password):
        return jsonify(Event0(token=token))
    else:
        return jsonify(Event1002())


@admin.route('/logout', methods=['POST'])
@admin_login
def adminLogout(token):
    if r.get(token) is None:
        return jsonify(Event1001())  # token无效
    try:
        r.delete(token)
        return jsonify(Event0())
    except:
        return jsonify(Event1005('token未成功删除'))
