
from app.User import user,jsonify,request,current_app,random_filename,db,os,send_email,login_required,method_verify
from app.User import User,Drama,Photo,Comment,Likedrama,Collectdrama,r,Anime,Follow
from app.User import Event0,Event1001,Event1002,Event1003,Event1004,Event1005,HOST

@user.route('/follows',methods=['POST','DELETE'])
@login_required
def follows(token):
    if request.method == 'POST':
        userid = request.form.get('userid')
        user = User.query.get(r.get(token))
        if User.query.get(userid) is None:
            return jsonify(Event1002())
        if user.follower.filter_by(followerid=userid).first() is not None:
            return jsonify(Event1005('你已关注该用户'))
        follow = Follow(followerid=userid,followedid=r.get(token))
        db.session.add(follow)
        db.session.commit()
        return jsonify(Event0(token=token))
    elif request.method == 'DELETE':
        followid = request.form.get('userid')
        user = User.query.get(r.get(token))
        if User.query.get(followid) is None:
            return jsonify(Event1005('该用户不存在'))
        if user.follower.filter_by(followerid=followid).first() is None:
            return jsonify(Event1005('未关注该用户'))
        follow = user.follower.filter_by(followerid=followid).first()
        db.session.delete(follow)
        db.session.commit()
        return jsonify(Event0(token=token))


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
            return jsonify(Event1003())
        if User.query.filter_by(email=email).first() is not None:        #邮箱存在，返回错误
            return jsonify(Event1005('邮箱已被注册'))
        if password == repeatpd:
            user = User(
                name=name,
                password=password,
                email=email
            )
            db.session.add(user)
            db.session.commit()
            if avatar and avatar.filename != '':
                avatar.filename = random_filename(avatar.filename)
                avatar.save(os.path.join(current_app.config['UPLOAD_PATH'], avatar.filename))
                user.avatar = 'http://' + HOST + '/user/image/' + avatar.filename
            db.session.commit()
            send_email('注册成功',user.email,'注册成功欢迎加入我们')
            token = user.make_token()
            r.set(token,str(user.id))
            return jsonify(Event0(token=token))
        return jsonify(Event1005('密码不一致'))
    return jsonify(Event1004())


#推荐表测试
@user.route('/recommend',methods=['POST','DELETE'])
@login_required
def recomment(token):
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        animepicture = request.files.getlist('animepicture')
        photo = request.files.getlist('photo')
        animetitle = request.form.get('animetitle')
        user_id = r.get(token)
        describe = request.form.get('describe')
        datafrom = request.form.get('datafrom')
        link = request.form.get('link')
        seasonid = request.form.get('seasonid')
        tag1 = request.form.get('tag1')
        tag2 = request.form.get('tag2')
        tag3 = request.form.get('tag3')
        if int(datafrom) == 1:
            drama = Drama(title=title, content=content, user_id=user_id)
            db.session.add(drama)
            db.session.commit()
            anime = Anime(title=animetitle,describe=describe,datafrom=datafrom,seasonId=seasonid,dramaid=drama.id,tag1=tag1,tag2=tag2,tag3=tag3)
            db.session.add(anime)
        elif int(datafrom) == 2:
            drama = Drama(title=title, content=content, user_id=user_id)
            db.session.add(drama)
            db.session.commit()
            anime = Anime(title=animetitle,describe=describe, link=link,datafrom=datafrom, dramaid=drama.id,tag1=tag1,tag2=tag2,tag3=tag3)
            db.session.add(anime)
        db.session.commit()
        for file in animepicture:
            file.filename = random_filename(file.filename)
            coverp = Photo(image= 'http://' + HOST + '/user/image/' + file.filename, drama_id=drama.id, cover=True)
            file.save(os.path.join(current_app.config['UPLOAD_PATH'], file.filename))
            anime.picture = coverp.image
            db.session.add(coverp)
        for file in photo:
            file.filename = random_filename(file.filename)
            contentp = Photo(image='http://' + HOST + '/user/image/' + file.filename, drama_id=drama.id, content=True)
            file.save(os.path.join(current_app.config['UPLOAD_PATH'], file.filename))
            db.session.add(contentp)
        db.session.commit()
        user = User.query.get(r.get(token))
        for follow in user.followed.all():
            send_email('你关注的用户更新啦',follow.followed.email,follow.followed.name+'——'+'['+title+']'+'(推荐番)')
        return jsonify(Event0(token=token, dramaid=drama.id))
    elif request.method == 'DELETE':
        dramaid = request.form.get('dramaid')
        drama = Drama.query.get(dramaid)
        if drama is None:
            return jsonify(Event1002())
        db.session.delete(drama)
        db.session.commit()
        if Drama.query.get(dramaid) is not None:
            return jsonify(Event1005('删除失败'))
        return jsonify(Event0(token=token))
    return jsonify(Event1004())


@user.route('/recommend/comment',methods=['POST','DELETE'])
@login_required
def comment(token):
    if request.method == 'POST':
        drama_id = request.form.get('dramaid')
        text = request.form.get('content')
        user = User.query.get(r.get(token))
        reply = request.form.get('reply')
        commentid =request.form.get('commentid')
        if Drama.query.get(drama_id) is None:
            return jsonify(Event1002())
        if reply == 'true':
            drama = Drama.query.get(drama_id)
            comment = Comment.query.get(commentid)
            if comment is None:
                return jsonify(Event1002())
            reply = Comment(drama_id=drama_id,text='@' + str(comment.author) + '  ' + text,author_id=user.id,author=user.name,email=user.email)
            db.session.add(reply)
            db.session.commit()
            send_email(drama.title,comment.email,
                       '你的评论' + '[' + comment.text + ']有新的回复:' + str(reply.author) + ' ' +str(reply.text) 
                       )
            return jsonify(Event0(token=token))
        comment = Comment(drama_id=drama_id, text=text, author_id=user.id, author=user.name,email=user.email)
        db.session.add(comment)
        db.session.commit()
        likes = Likedrama.query.filter(Likedrama.drama_id==drama_id,Likedrama.follow==True).all()
        for like in likes:
            send_email(like.drama.title,like.user.email,'你关注的问题有新的评论：['+text+']')
        return jsonify(Event0(token=token))
    elif request.method == 'DELETE':
        commentid = request.form.get('commentid')
        comment = Comment.query.get(commentid)
        if comment is None:
            return jsonify(Event1002())
        db.session.delete(comment)
        db.session.commit()
        if Comment.query.get(commentid) is not None:
            return jsonify(Event1005('删除失败'))
        return jsonify(Event0(token=token))
    return jsonify(Event1004())



@user.route('/recommend/star',methods=['POST','DELETE'])
@login_required
def star(token):
    if request.method == 'POST':
        dramaid = request.form.get('dramaid')
        if Likedrama.query.filter_by(user_id=r.get(token),drama_id=dramaid).first() is not None:
            return jsonify(Event1003())
        if Drama.query.filter(Drama.id==dramaid,Drama.solution==None).first():
            star = Likedrama(user_id=r.get(token), drama_id=dramaid)
            db.session.add(star)
            db.session.commit()
            if Likedrama.query.get(star.id) is not None:
                return jsonify(Event0(token=token))
            return jsonify(Event1005('创建失败'))
        elif Drama.query.filter(Drama.id==dramaid,Drama.solution!=None).first():
            star = Likedrama(user_id=r.get(token), drama_id=dramaid,follow=True)
            db.session.add(star)
            db.session.commit()
            if Likedrama.query.get(star.id) is not None:
                return jsonify(Event0(token=token))
            return jsonify(Event1005('创建失败'))
        else:
            return jsonify(Event1002())
    elif request.method == 'DELETE':
        dramaid = request.form.get('dramaid')
        star = Likedrama.query.filter_by(user_id=r.get(token),drama_id=dramaid).first()
        if star is None:
            return jsonify(Event1002())
        db.session.delete(star)
        db.session.commit()
        if Likedrama.query.get(star.id) is not None:
            return jsonify(Event1005('删除失败'))
        return jsonify(Event0(token=token))

@user.route('/recommend/collect',methods=['POST','DELETE'])
@login_required
def collect(token):
    if request.method == 'POST':
        dramaid = request.form.get('dramaid')
        if Drama.query.get(dramaid) is None:
            return jsonify(Event1002())
        if Collectdrama.query.filter_by(user_id=r.get(token), drama_id=dramaid).first() is not None:
            return jsonify(Event1003())
        collect = Collectdrama(user_id=r.get(token), drama_id=dramaid)
        db.session.add(collect)
        db.session.commit()
        if Collectdrama.query.get(collect.id) is not None:
            return jsonify(Event0(token=token))
        return jsonify(Event1005('创建失败'))
    elif request.method == 'DELETE':
        dramaid = request.form.get('dramaid')
        collect = Collectdrama.query.filter_by(user_id=r.get(token),drama_id=dramaid).first()
        if collect is None:
            return jsonify(Event1002())
        db.session.delete(collect)
        db.session.commit()
        if Collectdrama.query.get(collect.id) is not None:
            return jsonify(Event1005('删除失败'))
        return jsonify(Event0(token=token))
    return jsonify(Event1004())

@user.route('/ask',methods=['POST','DELETE'])
@login_required
def ask(token):
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        photos = request.files.getlist('photos')
        userid = r.get(token)
        drama = Drama(title=title, content=content, solution='false',user_id=userid)
        db.session.add(drama)
        db.session.commit()
        for file in photos:
            file.filename = random_filename(file.filename)
            contentp = Photo(image='http://' + HOST + '/user/image/' + file.filename, drama_id=drama.id, content=True)
            file.save(os.path.join(current_app.config['UPLOAD_PATH'], file.filename))
            db.session.add(contentp)
        db.session.commit()
        user = User.query.get(r.get(token))
        for follow in user.followed.all():
            send_email('你关注的用户更新啦', follow.followed.email, follow.followed.name + '——' + '[' + title + ']' + '(推荐番)')
        return jsonify(Event0(token=token, dramaid=drama.id))
    if request.method == 'DELETE':
        dramaid = request.form.get('dramaid')
        drama = Drama.query.get(dramaid)
        if drama is None:
            return jsonify(Event1002())
        db.session.delete(drama)
        db.session.commit()
        if Drama.query.get(dramaid) is not None:
            return jsonify(Event1005('删除失败'))
        return jsonify(Event0(token=token))
    return jsonify(Event1004())


@user.route('/ask/solve',methods=['POST','DELETE'])
@login_required
def solve(token):
    if request.method == 'POST':
        dramaid = request.form.get('dramaid')
        drama = Drama.query.get(dramaid)
        if drama is None:
            return jsonify(Event1002())
        if drama.solution is None:
            return jsonify(Event1005('对象不是可关注对象'))
        if drama.solution == 'true':
            return jsonify(Event1005('已处于解决状态'))
        drama.solution = 'true'
        db.session.commit()
        return jsonify(Event0(token=token))
    elif request.method == 'DELETE':
        dramaid = request.form.get('dramaid')
        drama = Drama.query.get(dramaid)
        if drama is None:
            return jsonify(Event1002())
        if drama.solution is None:
            return jsonify(Event1005('对象不是可关注对象'))
        if drama.solution == 'false':
            return jsonify(Event1005('已处于未解决状态'))
        drama.solution = 'false'
        db.session.commit()
        return jsonify(Event0(token=token))




