
from app.User import user,jsonify,request,current_app,random_filename,User,db,os,send_email
from app.User import User,Drama,Photo,Comment,Likedrama,Collectdrama

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


#推荐表测试
@user.route('/recommend',methods=['POST'])
def recomment():
    title = request.form.get('title')
    content = request.form.get('content')
    coverphotos = request.files.getlist('coverphotos')
    contentphotos = request.files.getlist('contentphotos')
    print(coverphotos,contentphotos)
    user_id = request.form.get('user_id')
    synopsis = request.form.get('synopsis')
    bvid = request.form.get('bvid')
    web = request.form.get('web')
    drama = Drama(title=title,content=content,user_id=user_id,synopsis=synopsis,bvid=bvid,web=web)
    db.session.add(drama)
    db.session.commit()
    for file in coverphotos:
        file.filename = random_filename(file.filename)
        coverp = Photo(image=file.filename,drama_id=drama.id,cover=True)
        file.save(os.path.join(current_app.config['UPLOAD_PATH'], file.filename))
        db.session.add(coverp)
        db.session.commit()
    for file in contentphotos:
        file.filename = random_filename(file.filename)
        contentp = Photo(image=file.filename, drama_id=drama.id, content=True)
        file.save(os.path.join(current_app.config['UPLOAD_PATH'], file.filename))
        db.session.add(contentp)
        db.session.commit()
    #db.session.commit()
    print(drama.id,drama.title,drama.content,drama.synopsis,drama.user,drama.likes,drama.time,drama.solution,drama.bvid,drama.collects,drama.photos,drama.web)
    return jsonify({'event':'success'})


#评论表测试
@user.route('/comment',methods=['POST'])
def comment():
    drama_id = request.form.get('drama_id')
    text = request.form.get('text')
    author_id = request.form.get('author_id')
    author = request.form.get('author')
    comment = Comment(drama_id=drama_id,text=text,author_id=author_id,author=author)
    db.session.add(comment)
    db.session.commit()
    print(comment.id,comment.author,comment.drama,comment.author_id,comment.text)
    return jsonify({'event':'success'})

#关注表测试
@user.route('/follow',methods=['POST'])
def follow():
    follow_id = request.form.get('follow_id')
    user_id = request.form.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    user.follow_id = follow_id
    db.session.commit()
    print(user.follows)
    return jsonify({'event':'success'})


#点赞和收藏表测试
@user.route('/like_or_collect',methods=['POST'])
def like():
    user_id = request.form.get('user_id')
    drama_id = request.form.get('drama_id')
    like = Likedrama(user_id=user_id,drama_id=drama_id)
    collect = Collectdrama(user_id=user_id,drama_id=drama_id)
    db.session.add(like)
    db.session.add(collect)
    db.session.commit()
    user = User.query.get(user_id)
    drama = Drama.query.get(drama_id)
    print(user.likes,user.collects)
    print(drama.likes,drama.collects)
    return jsonify({'event':'success'})


