from app.Admin import admin
from app.Admin.AnimeDatas import Animedatas
from app.extensions import *
from app.models import *
from sqlalchemy import or_


def isIn(name, default):
    data = request.form.get(name)
    if data is not None:
        return data
    else:
        return default

# 获取全部番
# 做个分页
# 返回 封面 标题 标签
@admin.route('/anime/getall', methods=['POST'])
@admin_login
def getAllAnime(token):
    adminId = r.get(token)
    try:
        page = int(request.form.get('page'))

    except:
        return jsonify(Event1004())
    tagId = request.form.get('tagid')
    isShow = request.form.get('isshow')
    animes = Anime.query.all()
    if isShow is not None:
        animes = Anime.query.filter_by(isShow=int(isShow))
    if tagId is not None:
        animes = animes.filter(or_(Anime.tag1 == tagId, Anime.tag2 == tagId, Anime.tag3 == tagId))
    animes = animes.paginate(per_page=10, page=page)
    datalist = []
    for anime in animes.items:
        temp = {
            'id': anime.id,
            'title': anime.title,
            'picture': anime.picture,
            'likenum': anime.likenum,
            'tag1': anime.tag1,
            'tag2': anime.tag2,
            'tag3': anime.tag3
        }
        datalist.append(temp)
    return jsonify(
        {
            "status": 0,
            "data": {
                "totalnum": animes.pages,
                "hasnext": animes.has_next,
                "haspre": animes.has_prev,
                "datalist": datalist
            }
        }
    )



# 对单个anime的查删改
@admin.route('/anime/operate', methods=['GET', 'POST', 'DELETE', 'PUT'])
@admin_login
def operateAnime(token):
    # 获取到单个anime
    if request.method == 'GET':
        animeId = int(request.args.get("animeid"))
        anime = Anime.query.get(animeId)
        commentlist = []
        for comment in anime.comments:
            temp = {
                'commentid': comment.id,
                'username': comment.user.name,
                'comment': comment.comment,
                # 时间
                'time': comment.time,
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
                "status": 0,
                "data": data
            }
        )
        pass
    adminId = r.get(token)
    animeId = int(request.form.get('animeid'))
    if animeId is not None:
        anime = Anime.query.get(animeId)
    else:
        return jsonify(Event1004())
    # 手动增加一个anime
    if request.method == 'POST':
        anime.seasonId = isIn('seasonid', anime.seasonId)
        anime.mediaId = isIn('mediaid', anime.mediaId)
        anime.picture = isIn('picture', anime.picture)
        anime.title = isIn('title', anime.title)
        anime.describe = isIn('describe', anime.describe)
        anime.isShow = isIn('isshow', anime.isShow)
        anime.link = isIn('link', anime.link)
        anime.isFinish = isIn('isfinish', anime.isFinish)
        anime.tag1 = isIn('tag1', anime.tag1)
        anime.tag2 = isIn('tag2', anime.tag2)
        anime.tag3 = isIn('tag3', anime.tag3)
        anime.datafrom = isIn('datafrom', anime.datafrom)
        anime.likenum = isIn('likenum', anime.likenum)
        db.session.commit()
        return jsonify(Event0(token=token))
    # 手动删除一个anime
    elif request.method == 'DELETE':
        db.session.delete(anime)
        db.session.commit()
        return jsonify(Event0(token=token))
    # 手动修改一个anime
    elif request.method == 'PUT':
        anime.seasonId = isIn('seasonid', anime.seasonId)
        anime.mediaId = isIn('mediaid', anime.mediaId)
        anime.picture = isIn('picture', anime.picture)
        anime.title = isIn('title', anime.title)
        anime.describe = isIn('describe', anime.describe)
        anime.isShow = isIn('isshow',anime.isShow)
        anime.link = isIn('link', anime.link)
        anime.isFinish = isIn('isfinish', anime.isFinish)
        anime.tag1 = isIn('tag1', anime.tag1)
        anime.tag2 = isIn('tag2', anime.tag2)
        anime.tag3 = isIn('tag3', anime.tag3)
        anime.datafrom = isIn('datafrom', anime.datafrom)
        anime.likenum = isIn('likenum', anime.likenum)
        db.session.commit()
        return jsonify(Event0(token=token))


# 增加推荐anime, 减少推荐anime
@admin.route('/anime/ifshow', methods=['POST', 'DELETE'])
@admin_login
def ifShowAnime(token):
    adminId = r.get(token)
    animeId = int(request.form.get('animeid'))
    if animeId is not None:
        anime = Anime.query.get(animeId)
    else:
        return jsonify(Event1004())
    if request.method == 'POST':
        if anime.isShow is False:
            anime.isShow = True
            db.session.commit()
            return jsonify(Event0(token=token))
        else:
            return jsonify(Event1005("已经设为展示了"))
    elif request.method == 'DELETE':
        if anime.isShow is True:
            anime.isShow = False
            db.session.commit()
            return jsonify(Event0(token=token))
        else:
            return jsonify(Event1005("已经设为不展示了"))


@admin.route('/anime/comment', methods=['POST', 'DELETE'])
@admin_login
def animeComment(token):
    commentId = request.form.get('commentid')
    comment = AnimeComment.query.get(commentId)
    if comment is None:
        return jsonify(Event1004())
    if request.method == 'POST':
        return jsonify(
            {
                "status": 0,
                "data": {
                    "userid": comment.user.id,
                    "username": comment.user.name,
                    "text": comment.comment,
                    "time": comment.time,
                    "starnum": comment.starnum
                }
            }
        )
    elif request.method == 'DELETE':
        db.session.delete(comment)
        db.session.commit()
        return jsonify(Event0(token=token))



# 刷新完结动画推荐
# 原先的不会删除，会被标记为不显示
@admin.route('/anime/refresh', methods=['GET'])
def refreshFinishedAnime():
    # adminLoginConfirm(name)

    # 设置原先不显示
    # oldDatas = Anime.query.filter_by(isShow=True, datafrom=1)
    # for oldData in oldDatas:
    #     oldData.isShow = False

    # 添加爬取的新数据
    datas = Animedatas
    for data in datas:
        newData = Anime(
            title=data['title'],
            picture=data['picture'],
            describe=data['describe'],
            seasonId=data['seasonId'],
            mediaId=data['mediaId'],
            link=data['link'],
            isFinish=data['isFinish'],
            tag1=data['tag'],
            datafrom=1,
            isShow=True
        )
        db.session.add(newData)
    db.session.commit()
    return jsonify(Event0())
