from app.User import user,login_required,request,pickle,r,random_filename,os,current_app,db,jsonify,User



#login_required为登录验证装饰器，在extensions.py文件中
@user.route('/updata',methods=['PUT'])
@login_required
def updata():
    name = request.form.get('name')
    avatar = request.files.get('avatar')
    password = request.form.get('password')
    repeatpd = request.form.get('repeatpd')
    email = request.form.get('email')
    user = User.query.filter_by(id=r.get('user')).first()
    if name is not None:
        user.name = name
    if avatar is not None:
        avatar.filename = random_filename('user' + str(user.id) + os.path.splitext(avatar.filename)[1])
        avatar.save(os.path.join(current_app.config['UPLOAD_PATH'], avatar.filename))
        user.avatar = avatar.filename
    if password is not None and password == repeatpd:
        user.password = password
    if email is not None:
        user.email = email
    db.session.commit()
    return jsonify({'event':'success'})