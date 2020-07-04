from flask import jsonify, request
from app.Anime import anime
from app.models import *


@anime.route('/getallanime', methods=['GET', 'POST'])
def getAllAnime():
    if request.method == 'GET':
        datas = Anime.query.filter_by(isShow=True).all()

    elif request.method == 'POST':
        tagId = request.form.get('tagid')
        datas = Anime.query.filter_by(isShow=True, tag=tagId).all()
    else:
        return jsonify(
            {
                'status': 1001,
                'message': "请求方式错误"
            }
        )
    if datas is []:
        return jsonify(
            {
                'status': 1002,
                'message': "请求数据错误"
            }
        )
    datalist = []
    for data in datas:
        temp = {
            'title': data.title,
            'picture': data.picture,
            'describe': data.describe,
            'seasonId': data.seasonId,
            'mediaId': data.mediaId,
            'link': data.link,
            'isFinish':data.isFinish,
            'tag': data.tag
        }
        datalist.append(temp)
    return jsonify(
        {
            'status': 0,
            'data': datalist
        }
    )