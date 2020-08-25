from app.Admin import admin
from app.extensions import *
from app.models import *


@admin.route('/recommend/getall', methods=['POST'])
@admin_login
def getAllRecommend(token):
    adminId = r.get(token)
    admin = Admin.query.get(adminId)
    try:
        page = int(request.form.get('page'))
        recommends = Drama.query.filter(Drama.solution == None).paginate(per_page=10, page=page)
    # 判断请求是否正确
    except:
        return jsonify(Event1004())
    datalist = []
    for recommend in recommends.items:
        data = {
            "authorname": recommend.user.name,
            "authorid": recommend.user.id,
            "dramaid": recommend.id,
            "title": recommend.title
        }
        datalist.append(data)
    return jsonify(
        {
            "status": 0,
            "data": {
                "totalnum": recommends.pages,
                "hasnext": recommends.has_next,
                "haspre": recommends.has_prev,
                "datalist": datalist
            }
        }
    )



@admin.route('/recommend/operate', methods=['POST', 'DELETE', 'PUT'])
@admin_login
def operateRecommend(token):
    adminId = r.get(token)
    admin = Admin.query.get(adminId)
    try:
        recommendId = int(request.form.get('recommendid'))
        recommend = Drama.query.get(recommendId)
    # 判断请求正确
    except:
        return jsonify(Event1004())
    if recommend is None:
        return jsonify(Event1002())
    # 获取当个详细
    if request.method == 'POST':
        photos = Photo.query.filter_by(drama_id=recommend.id, content=True).all()
        animepictures = Photo.query.filter_by(drama_id=recommend.id, cover=True).first()
        data =  {
            "dramaid": recommend.id,
            "authorid": recommend.user.id,
            "authorname": recommend.user.name,
            "title": recommend.title,
            "content": recommend.content,
            "time": recommend.time,
            "cover": animepictures.image,
            "photos": [photo.image for photo in photos],
            "animeid": recommend.anime[0].id,
            "comment": [Givecomment(comment) for comment in recommend.comments]
        }
        return jsonify(
            {
                "status": 0,
                "data": data
            }
        )
    # 发邮件提醒，删番
    elif request.method == 'DELETE':
        question = request.form.get('question')
        # 提示添加问题
        if question is None:
            return jsonify(Event1004())
        message = "您的标题为" + recommend.title + "的问番因" + question + "被管理员删除，特此予以警告"
        send_email("警告", recommend.user.email, message)
        db.session.delete(recommend)
        db.session.commit()

        return jsonify(Event0(token=token))


@admin.route('/recommend/comment', methods=['POST', 'DELETE'])
@admin_login
# 查，删
def recommendComment(token):
    adminId = r.get(token)
    admin = Admin.query.get(adminId)
    try:
        commentId = int(request.form.get('commentid'))
        comment = Comment.query.get(commentId)
    # 请求是否正确
    except:
        return jsonify(Event1004())

    # 返回无对象
    if comment is None:
        return jsonify(Event1002())
    if request.method == 'POST':
        data = {
            "commentid": comment.id,
            "dramatitle": comment.drama.title,
            "dramaid": comment.drama.id,
            "authorname": comment.author,
            "authorid": comment.author_id,
            "content": comment.text,
            "time": comment.time
        }
        return jsonify(
            {
                "status": 0,
                "data": data
            }
        )
    elif request.method == 'DELETE':
        question = request.form.get('question')
        # 记得添加原因
        if question is None:
            return jsonify(Event1004())
        message = "您的在标题为" + comment.drama.title + "下的的评论因" + question + "被管理员删除，特此予以警告"
        user = User.query.get(comment.author_id)
        send_email("警告", user.email, message)
        db.session.delete(comment)
        db.session.commit()
        return jsonify(Event0(token=token))