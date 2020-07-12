from app.User import user,request,jsonify,User,login_required,r
from app.User import Event0,Event1001,Event1002,Event1003,Event1004,Event1005

<<<<<<< HEAD
#过期时间
EX_TIME = 3600
=======
>>>>>>> f4eceed929deec1ee461d6d1cb9a0c52d7f8b35d


#登录URL
@user.route('/login',methods=['POST'])
def login():
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter_by(name=name,password=password).first()
    if user is not None:
        token = user.make_token()       #加密
<<<<<<< HEAD
        r.set(token,str(user.id),ex=EX_TIME)
=======
        r.set(token,str(user.id))
>>>>>>> f4eceed929deec1ee461d6d1cb9a0c52d7f8b35d
        return jsonify(Event0(token=token))
    return jsonify(Event1002())


#登出url,存在登录限制
@user.route('/logout',methods=['POST'])
@login_required
def logout(token):
    if r.get(token) is None:
        return jsonify(Event1001())     #过期返回
    r.delete(token)
    if r.get(token) is None:                #删除返回
        return jsonify(Event0())
    return jsonify(Event1005('token未成功删除'))





