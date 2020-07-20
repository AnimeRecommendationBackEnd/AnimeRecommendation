from app.Admin import admin
from app.extensions import *
from app.models import *


@admin.route('getallrecommend', methods=['POST'])
@admin_login
def getAllRecommend(token):
    adminId = r.get(token)
    admin = Admin.query.get(adminId)
    page = request.form.get('page')
    solution = request.form.get('solution')
    if solution is not None:
        recommends = Drama.query.filter(Drama.solution == solution).paginate(per_page=10, page=page).items
    else:
        recommends = Drama.query.filter(Drama.solution != None).paginate(per_page=10, page=page).items
    datalist = []
    for recommend in recommends:
        data = Givep_recommentd(recommend)
        datalist.append(data)
    return jsonify(
        {
            "status": 0,
            "data": datalist
        }
    )



@admin.route('operaterecommend', methods=['POST', 'DELETE', 'PUT'])
@admin_login
def operateRecommend(token):
    adminId = r.get(token)
    admin = Admin.query.get(adminId)
    recommendId = request.form.get('recommendid')
    recommend = Drama.query.get(recommendId)
    # 获取当个详细
    if request.method == 'POST':
        data = Givedrama(recommend)
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


@admin.route('/recommendcomment', methods=['PSOT', 'DELETE'])
@admin_login
# 查，删
def recommendComment(token):
    adminId = r.get(token)
    admin = Admin.query.get(adminId)
    commentId = request.form.get('commentid')
    comment = Drama.query.get(commentId)
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