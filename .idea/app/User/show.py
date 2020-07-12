from app.User import user,jsonify,request,current_app,random_filename,db,os,send_email,login_required,send_from_directory
from app.User import User,Drama,Photo,Comment,Likedrama,Collectdrama,r
from app.User import Event0,Event1001,Event1002,Event1003,Event1004,Event1005
<<<<<<< HEAD
from app.User import Givedrama,Giveask,Giveuser
=======
from app.User import Givedrama,Giveask,Giveuser,Giveperson,Givep_recommentd,Givep_ask
>>>>>>> f4eceed929deec1ee461d6d1cb9a0c52d7f8b35d

@user.route('/get',methods=['GET'])
def Getuser():
    userid = request.form.get('userid')
    ask = request.form.get('ask')
    page = request.form.get('page',1,type=int)
    if userid is not None:
        user = User.query.get(userid)
        if user is None:
            return jsonify(Event1002())
        return jsonify({
            "status": 0,
            "data": [Giveuser(user)]
        })
    if ask is not None:
        pagination = User.query.whooshee_search(ask).paginate(page,5,error_out=False)
        results = pagination.items
        if results:
            return jsonify({
                "status": 0,
                "count": len(results),
                "data": [Giveuser(user) for user in results]
            })
        return jsonify(Event1002())
    pagination = User.query.paginate(page, 5, error_out=False)
    users = pagination.items
    if users:
        return jsonify({
            "status": 0,
            "count": len(users),
            "data": [Giveuser(user) for user in users]
        })
    return jsonify(Event1002())


@user.route('/recommend/get',methods=['GET'])
def GetRecommend():
    dramaid = request.form.get('dramaid')
    ask = request.form.get('ask')
    page = request.form.get('page',1,type=int)
    if dramaid is not None:
        drama = Drama.query.get(dramaid)
        if drama is not None and drama.solution == None:
            return jsonify({
                        "status": 0,
                        "data": [Givedrama(drama)]
                    })
        return jsonify(Event1002())
    if ask is not None:
        pagination = Drama.query.filter(Drama.solution==None).whooshee_search(ask).paginate(page,5,error_out=False)
        results = pagination.items
        if results:
            return jsonify({
                        "status": 0,
                        "count": len(results),
                        "data": [Givedrama(drama) for drama in results]
                    })
        return jsonify(Event1002())
    pagination = Drama.query.filter(Drama.solution==None).paginate(page, 5 ,error_out=False)
    dramas = pagination.items
    if dramas:
        return jsonify({
                        "status": 0,
                        "count": len(dramas),
                        "data": [Givedrama(drama) for drama in dramas]
                    })
    return jsonify(Event1002())


@user.route('/ask/get',methods=['GET'])
def GetAsk():
    dramaid = request.form.get('dramaid')
    ask = request.form.get('ask')
    page = request.form.get('page', 1, type=int)
    if dramaid is not None:
        drama = Drama.query.get(dramaid)
        if drama is not None and drama.solution != None:
            return jsonify({
            "status": 0,
            "data": [Giveask(drama)]
        })
        return jsonify(Event1002())
    if ask is not None:
        pagination = Drama.query.filter(Drama.solution!=None).whooshee_search(ask).paginate(page, 5,error_out=False)
        results = pagination.items
        if results:
            return jsonify({
            "status": 0,
            "count": len(results),
            "data": [Giveask(drama) for drama in results]
        })
        return jsonify(Event1002())
    pagination = Drama.query.filter(Drama.solution!=None).paginate(page, 5,error_out=False)
    dramas = pagination.items
    if dramas:
        return jsonify({
        "status": 0,
        "count": len(dramas),
        "data": [Giveask(drama) for drama in dramas]
    })
    return jsonify(Event1002())

@user.route('/image/<path:filename>',methods=['GET'])
def index(filename):
<<<<<<< HEAD
    return send_from_directory(current_app.config['UPLOAD_PATH'], filename,as_attachment=True)
=======
    return send_from_directory(current_app.config['UPLOAD_PATH'], filename,as_attachment=True)

@user.route('/person',methods=['GET'])
@login_required
def person(token):
    user = User.query.get(r.get(token))
    return jsonify({
        "status": 0,
        "data": Giveuser(user)
    })

@user.route('/person/fans',methods=['GET'])
@login_required
def fans(token):
    userid = request.form.get('userid')
    if User.query.get(userid) is not None:
        user = User.query.get(userid)
        fans = user.followed.all()
        return jsonify({
            "status": 0,
            "count": len(fans),
            "data": [{'fanid': fan.followed.id, 'avatar': fan.followed.avatar, 'name': fan.followed.name} for fan in
                     fans]
        })
    user = User.query.get(r.get(token))
    fans = user.followed.all()
    return jsonify({
        "status": 0,
        "count": len(fans),
        "data": [{'fanid':fan.followed.id, 'avatar':fan.followed.avatar,'name':fan.followed.name} for fan in fans]
    })

@user.route('/person/follower',methods=['GET'])
@login_required
def followers(token):
    userid = request.form.get('userid')
    if User.query.get(userid) is not None:
        user = User.query.get(userid)
        followers = user.follower.all()
        return jsonify({
            "status": 0,
            "count": len(followers),
            "data": [
                {'followerid': follower.follower.id, 'avatar': follower.follower.avatar, 'name': follower.follower.name}
                for follower in followers]
        })
    user = User.query.get(r.get(token))
    followers = user.follower.all()
    return jsonify({
        "status": 0,
        "count": len(followers),
        "data": [{'followerid':follower.follower.id,'avatar':follower.follower.avatar,'name':follower.follower.name}for follower in followers]
    })

@user.route('/person/recommend',methods=['GET'])
@login_required
def P_recommend(token):
    userid = request.form.get('userid')
    if userid is not None:
        dramas = Drama.query.filter(Drama.user_id == userid, Drama.solution == None).all()
        return jsonify({
            "status": 0,
            "count": len(dramas),
            "data": [Givep_recommentd(drama) for drama in dramas]
        })
    dramas = Drama.query.filter(Drama.user_id==r.get(token),Drama.solution==None).all()
    return jsonify({
        "status": 0,
        "count": len(dramas),
        "data": [Givep_recommentd(drama) for drama in dramas]
    })

@user.route('/person/ask',methods=['GET'])
@login_required
def P_ask(token):
    userid = request.form.get('userid')
    if userid is not None:
        dramas = Drama.query.filter(Drama.user_id == userid, Drama.solution != None).all()
        return jsonify({
            "status": 0,
            "count": len(dramas),
            "data": [Givep_recommentd(drama) for drama in dramas]
        })
    dramas = Drama.query.filter(Drama.user_id == r.get(token), Drama.solution != None).all()
    return jsonify({
        "status": 0,
        "count": len(dramas),
        "data": [Givep_ask(drama) for drama in dramas]
    })
>>>>>>> f4eceed929deec1ee461d6d1cb9a0c52d7f8b35d
