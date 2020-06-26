from app.User import user,request,jsonify,User,random_redis_token,r,pickle

#过期时间
EX_TIME = 3600


@user.route('/login',methods=['POST'])
def login():
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter_by(name=name,password=password).first()
    if user is not None:
        r.set('user',str(user.id),ex=EX_TIME)
        return jsonify({'event':'success'})
    return jsonify({'error':'no user'})


