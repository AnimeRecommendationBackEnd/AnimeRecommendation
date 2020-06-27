
from app.User import user,jsonify,request,current_app,random_filename,User,db,os,send_email

#创建用户URL，用户名以及邮箱唯一
@user.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        repeatpd = request.form.get('repeatpd')
        avatar = request.files.get('avatar')
        email = request.form.get('email')
        if User.query.filter_by(name=name).first() is not None:         #用户名存在，返回错误
            return jsonify({'error':'user exited'})
        if User.query.filter_by(email=email).first() is not None:        #邮箱存在，返回错误
            return jsonify({'error':'email registered'})
        if password == repeatpd:
            user = User(
                name=name,
                password=password,
                email=email
            )
            db.session.add(user)
            db.session.commit()
            if avatar and avatar.filename != '':
                avatar.filename = random_filename('user' + str(user.id) + os.path.splitext(avatar.filename)[1])
                avatar.save(os.path.join(current_app.config['UPLOAD_PATH'], avatar.filename))
                user.avatar = avatar.filename
            db.session.commit()
            send_email('注册成功',user.email,'注册成功欢迎加入我们')
            return jsonify({'event': 'success'})
        return jsonify({'error': 'password error'})
    return jsonify({'error': 'method error'})

