from flask import jsonify, request
from app.Anime import anime
from app.models import *
from app.extensions import Event0, Event1001, Event1002, Event1003, Event1004, Event1005, login_required, r


@anime.route('/getallanime', methods=['GET', 'POST'])
def getAllAnime():
    # 分类
    if request.method == 'GET':
        datas = Anime.query.filter_by(isShow=True).all()

    elif request.method == 'POST':
        tagId = request.form.get('tagid')
        datas = Anime.query.filter_by(isShow=True, tag1=tagId).all() + Anime.query.filter_by(isShow=True, tag2=tagId).all() + Anime.query.filter_by(isShow=True, tag3=tagId).all()

    else:
        return jsonify(Event1004())
    if datas is []:
        return jsonify(Event1004())

    # 如果带token请求，就获取用户id
    token = request.form.get('token')
    userId = None
    if token is not None:
        userId = r.get(token)

    datalist = []
    for data in datas:
        # 根据animelike表查询是否点赞
        if userId and AnimeLike.query.filter_by(userId=userId, animeId=data.id).first() is not None:
            isLike = True
        else:
            isLike = False
        temp = {
            'id': data.id,
            'title': data.title,
            'picture': data.picture,
            'likenum': data.likenum,
            'islike': isLike,
            'tag1': data.tag1,
            'tag2': data.tag2,
            'tag3': data.tag3
        }
        datalist.append(temp)
    return jsonify(
        {
            'status': 0,
            'data': datalist
        }
    )


@anime.route('/getanime', methods=['GET', 'POST'])
def getAnime():
    if request.method == 'GET':
        animeId = request.args.get('animeid')
        anime = Anime.query.get(animeId)
        if anime is None:
            return jsonify(Event1002())
        commentlist = []
        for comment in anime.comments:
            temp = {
                'commentid': comment.id,
                'username': comment.user.name,
                'comment': comment.comment,
                # 时间
                # 'time': comment.time
                'starnum': comment.starnum,
            }
            commentlist.append(temp)
        data = {
            'id': anime.id,
            'title': anime.title,
            'picture': anime.picture,
            'describe': anime.describe,
            'seasonId': anime.seasonId,
            'mediaId': anime.mediaId,
            'link': anime.link,
            'isFinish': anime.isFinish,
            'likenum': anime.likenum,
            'islike': False,
            'comments': commentlist,
            'tag1': anime.tag1,
            'tag2': anime.tag2,
            'tag3': anime.tag3
        }
        return jsonify(
            {
                'status': 0,
                'data': data
            }
        )
    if request.method == 'POST':
        token = request.form.get('token')
        animeId = request.form.get('animeid')
        if token is None:
            return jsonify(Event1004())
        userId = r.get(token)
        if userId is None:
            return  jsonify(Event1001())
        anime = Anime.query.get(animeId)
        if anime is None:
            return jsonify(Event1002())
        commentlist = []
        for comment in anime.comments:
            if AnimeCommentStar.query.filter_by(animeCommentId=comment.id, userId=userId).first() is not None:
                isLike = True
            else:
                isLike = False
            temp = {
                'commentid': comment.id,
                'username': comment.user.name,
                'comment': comment.comment,
                'islike': isLike,
                # 时间
                # 'time': comment.time
                'starnum': comment.starnum,
            }
            commentlist.append(temp)
        data = {
            'id': anime.id,
            'title': anime.title,
            'picture': anime.picture,
            'describe': anime.describe,
            'seasonId': anime.seasonId,
            'mediaId': anime.mediaId,
            'link': anime.link,
            'isFinish': anime.isFinish,
            'likenum': anime.likenum,
            'islike': False,
            'comments': commentlist,
            'tag1': anime.tag1,
            'tag2': anime.tag2,
            'tag3': anime.tag3
        }
        return jsonify(
            {
                'status': 0,
                'data': data
            }
        )


@anime.route('/comment', methods=['POST', 'DELETE'])
@login_required
def AComment(token):
    if request.method == 'POST':
        comment = request.form.get('comment')
        animeId = request.form.get('animeid')
        userId = r.get(token)
        # 请求错误
        if comment is None or comment == '':
            return jsonify(Event1004())
        # 查询有没有这个id
        if Anime.query.get(animeId) is None:
            return jsonify(Event1002())
        animeComment = AnimeComment(
            userId=userId,
            comment=comment,
            animeId=animeId
        )
        db.session.add(animeComment)
        db.session.commit()
        return jsonify(Event0(token=token))
    elif request.method == 'DELETE':
        commentId = request.form.get('commentid')
        userId = r.get(token)
        comment = AnimeComment.query.get(commentId)
        # 查询是否有这个对象
        if comment is None:
            return jsonify(Event1002())
        elif comment.userId != int(userId):
            print(comment.userId, userId)
            return jsonify(Event1005("你不是作者"))
        db.session.delete(comment)
        db.session.commit()
        return jsonify(Event0(token=token))
    else:
        return jsonify(Event1004())


@anime.route('/like', methods=['POST', 'DELETE'])
@login_required
def AnimeStar(token):
    userId = r.get(token)
    animeId = request.form.get('animeid')
    # 查询有没有这个id
    anime = Anime.query.get(animeId)
    if anime is None:
        return jsonify(Event1002())
    if request.method == 'POST':
        if AnimeLike.query.filter_by(userId=userId, animeId=animeId).first() is not None:
            return jsonify(Event1005("不能重复点赞"))
        animeLike = AnimeLike(
            userId=userId,
            animeId=animeId
        )
        anime.likenum += 1
        db.session.add(animeLike)
        db.session.commit()
        return jsonify(Event0(token=token))

    elif request.method == 'DELETE':
        animelike = AnimeLike.query.filter_by(userId=userId, animeId=animeId).first()
        if animelike is None:
            return jsonify(Event1002())
        db.session.delete(animelike)
        anime.likenum -= 1
        db.session.commit()
        return jsonify(Event0(token=token))
    else:
        return jsonify(Event1004())



@anime.route('/comment/star', methods=['POST', 'DELETE'])
@login_required
def ACStar(token):
    userId = r.get(token)
    animeCommentId = request.form.get('commentid')
    animecomment = AnimeComment.query.get(animeCommentId)
    if animecomment is None:
        return jsonify(Event1002())
    if request.method == 'POST':
        if AnimeCommentStar.query.filter_by(userId=userId, animeCommentId=animeCommentId).first() is not None:
            return jsonify(Event1005("不能重复点赞"))
        acstar = AnimeCommentStar(
            userId=userId,
            animeCommentId=animeCommentId
        )
        animecomment.starnum += 1
        db.session.add(acstar)
        db.session.commit()
        return jsonify(Event0(token=token))
    elif request.method == 'DELETE':
        acstar = AnimeCommentStar.query.filter_by(userId=userId, animeCommentId=animeCommentId).first()
        if acstar is None:
            return jsonify(Event1002())
        db.session.delete(acstar)
        animecomment.starnum -= 1
        db.session.commit()
        return jsonify(Event0(token=token))
    else:
        return jsonify(Event1004())