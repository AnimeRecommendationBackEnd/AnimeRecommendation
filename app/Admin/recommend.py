from app.Admin import admin
from app.extensions import *
from app.models import *


@admin.route('/getallrecommend', methods=['POST'])
@admin_login
def getAllRecommend(token):
    adminId = r.get(token)
    admin = Admin.query.get(adminId)
    page = int(request.form.get('page'))
    recommends = Drama.query.filter(Drama.solution == None).paginate(per_page=10, page=page).items
    datalist = []
    for recommend in recommends:
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
            "data": datalist
        }
    )



@admin.route('/operaterecommend', methods=['POST', 'DELETE', 'PUT'])
@admin_login
def operateRecommend(token):
    adminId = r.get(token)
    admin = Admin.query.get(adminId)
    recommendId = request.form.get('recommendid')
    recommend = Drama.query.get(recommendId)
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
        print(data)
        return jsonify(
            {
                "status": 0,
                "data": data
            }
        )
    # 发邮件提醒，删番
    elif request.method == 'DELETE':
        question = request.form.get('question')
        message = "您的标题为" + recommend.title + "的问番因" + question + "被管理员删除，特此予以警告"
        db.session.delete(recommend)
        db.session.commit()
        send_email("警告", recommend.user.email, message)
        return jsonify(Event0(token=token))


@admin.route('/recommendcomment', methods=['POST', 'DELETE'])
@admin_login
# 查，删
def recommendComment(token):
    adminId = r.get(token)
    admin = Admin.query.get(adminId)
    commentId = request.form.get('commentid')
    comment = Comment.query.get(commentId)
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
        message = "您的在标题为" + comment.drama.title + "下的的评论因" + question + "被管理员删除，特此予以警告"
        user = User.query.get(comment.author_id)
        send_email("警告", user.email, message)
        db.session.delete(comment)
        db.session.commit()
        return jsonify(Event0(token=token))