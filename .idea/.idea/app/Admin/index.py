from flask import redirect, url_for, render_template, jsonify

from app.Admin import admin
from app.Admin.login import adminLoginConfirm
from app.models import *
from app.Admin.form import *
from app.Admin.AnimeDatas import Animedatas


@admin.route('/index/<name>')
def adminIndex(name):
    adminLoginConfirm(name)
    AnimeDatas = Anime.query.filter_by(isShow=True)
    addfinishedAnimeForm = finishedAnimeForm()
    return render_template(
        'adminIndex.html',
        name=name,
        finishedAnimeDatas=AnimeDatas,
        addfinishedAnimeForm=addfinishedAnimeForm
    )


# 刷新完结动画推荐
# 原先的不会删除，会被标记为不显示
@admin.route('/index/refreshfinishedanime/<name>', methods=['get'])
def refreshFinishedAnime(name):
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
    return redirect(url_for('admin.adminIndex', name=name))


# 删除完结动画推荐
@admin.route('/index/deletefinishedanime/<name>/<int:id>', methods=['GET'])
def deleteFinishedAnime(name, id):
    adminLoginConfirm(name)

    data = Anime.query.get(id)
    data.isShow = False
    db.session.commit()
    return redirect(url_for('admin.adminIndex', name=name))
