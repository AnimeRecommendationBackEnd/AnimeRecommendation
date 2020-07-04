from app.User import user,jsonify,request,current_app,random_filename,db,os,send_email,login_required,send_from_directory
from app.User import User,Drama,Photo,Comment,Likedrama,Collectdrama,r
from app.User import Event0,Event1001,Event1002,Event1003,Event1004,Event1005
from app.User import Givedrama,Giveask,Giveuser

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
    return send_from_directory(current_app.config['UPLOAD_PATH'], filename,as_attachment=True)