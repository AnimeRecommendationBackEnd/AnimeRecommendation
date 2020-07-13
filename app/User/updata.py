from app.User import user,request,r,random_filename,os,current_app,db,jsonify,User,login_required,send_email
from app.User import Event0,Event1001,Event1002,Event1003,Event1004,Event1005



#login_required为登录验证装饰器，在extensions.py文件中
@user.route('/update',methods=['POST'])
@login_required
def updata(token):
    name = request.form.get('name')
    avatar = request.files.get('avatar')
    password = request.form.get('password')
    email = request.form.get('email')
    user = User.query.filter_by(id=r.get(token)).first()
    if name is not None:
        if User.query.filter_by(name=name).first() is not None:             #用户名存在，返回错误
            return jsonify(Event1003())
        user.name = name
    if avatar is not None:
        avatar.filename = random_filename('user' + str(user.id) + os.path.splitext(avatar.filename)[1])
        avatar.save(os.path.join(current_app.config['UPLOAD_PATH'], avatar.filename))
        user.avatar = 'http://101.200.157.252/user/image/' + avatar.filename
    if password is not None:
        user.password = password
    if email is not None:
        if User.query.filter_by(email=email).first() is not None:       #邮箱存在，返回错误
            return jsonify(Event1005('邮箱已被注册'))
        user.email = email
    db.session.commit()
    return jsonify(Event0(token=token))


#找回密码URL
@user.route('/search',methods=['POST'])
def search():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user is not None:
            send_email('找回密码',user.email,'你好，'+ str(user.name) + '你的密码是'+ str(user.password))
            return jsonify(Event0())
        return jsonify(Event1002())
    return jsonify(Event1004())
