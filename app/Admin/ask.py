from app.Admin import admin
from app.extensions import *
from app.models import *


@admin.route('getallask', methods=['POST'])
@admin_login
def getAllAsk(token):
    adminId = r.get(token)
    admin = Admin.query.get(adminId)
    page = request.form.get('page')
    solution = request.form.get('solution')
    if solution is not None:
        asks = Drama.query.filter(Drama.solution == solution).paginate(per_page=10, page=page).items
    else:
        asks = Drama.query.filter(Drama.solution != None).paginate(per_page=10, page=page).items
    datalist = []
    for ask in asks:
        data = Givep_ask(ask)
        datalist.append(data)
    return jsonify(
        {
            "status": 0,
            "data": datalist
        }
    )



@admin.route('operateask', methods=['POST', 'DELETE', 'PUT'])
@admin_login
def operateAsk(token):
    adminId = r.get(token)
    admin = Admin.query.get(adminId)
    askId = request.form.get('askid')
    ask = Drama.query.get(askId)
    # 获取当个详细
    if request.method == 'POST':
        data = Giveask(ask)
        return jsonify(
            {
                "status": 0,
                "data": data
            }
        )
    # 发邮件提醒，删番
    elif request.method == 'DELETE':
        question = request.form.get('question')
        message = "您的标题为" + ask.title + "的问番因" + question + "被管理员删除"
        send_email("警告", ask.user.email, message)


@admin.route('/askcomment')
@admin_login
# 查，删
def askComment(token):
    pass