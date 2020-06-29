from app.Admin import admin
from app.Admin.login import adminLoginConfirm
from app.Admin.form import *
from flask import flash, session, redirect, url_for, render_template, request
from app.models import *
from app.utils import *


@admin.route('/index/<name>')
def adminIndex(name):
    adminLoginConfirm(name)
    finishedAnimeDatas = finishedAnime.query.filter_by(isShow=True)
    return render_template('adminIndex.html', name=name, finishedAnimeDatas=finishedAnimeDatas)


@admin.route('/index/refreshfinishedanime/<name>', methods=['get'])
def refreshFinishedAnime(name):
    adminLoginConfirm(name)

    oldDatas = finishedAnime.query.filter_by(isShow=True)
    for oldData in oldDatas:
        oldData.isShow = False
    datas = getMsg(url1)
    for data in datas:
        newData = finishedAnime(
            bvid=data['bvid'],
            title=data['title'],
            picture=data['picture'],
            introduce=data['introduce'],
            createtime=data['createtime']
        )
        db.session.add(newData)
    db.session.commit()
    return redirect(url_for('admin.adminIndex', name=name))





