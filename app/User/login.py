from app.User import user,request,jsonify,User,login_required,r

#过期时间
EX_TIME = 100


#登录URL
@user.route('/login',methods=['POST'])
def login():
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter_by(name=name,password=password).first()
    if user is not None:
        token = user.make_token()       #加密
        r.set(token,str(user.id),ex=EX_TIME)
        return jsonify({'event':'success','token':token})
    return jsonify({'error':'no user or password error'})

#登出url,存在登录限制
@user.route('/logout',methods=['POST'])
@login_required
def logout(token):
    if r.get(token) is None:
        return jsonify({'event':'success'})     #过期返回
    r.delete(token)
    if r.get(token) is None:                #删除返回
        return jsonify({'event':'success'})
    return jsonify({'error':'no login'})





