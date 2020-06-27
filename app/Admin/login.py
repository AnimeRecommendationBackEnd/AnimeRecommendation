from app.Admin import admin
from app.Admin.form import *
from flask import flash, session, redirect, url_for, render_template, request
from app.models import *

def adminLoginConfirm(username):
    if session.get("username") != username:
        return redirect(url_for("admin.adminLogin", next=request.url))


@admin.route('/login', methods=['GET', 'POST'])
def adminLogin():
    form = adminLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        admin = Admin.query.filter_by(username=username)
        if admin.count() == 0:
            flash('用户不存在')

        else:
            print(admin.first().checkPassword(password))
            if admin.first().checkPassword(password):
                session['username'] = username
                return redirect(url_for('admin.adminIndex', username=username))
            else:
                flash('密码错误')

    return render_template('adminLogin.html', form=form)

@admin.route('/logout/<username>', methods=['GET'])
def adminLogout(username):
    # 身份验证
    adminLoginConfirm(username)
    session.pop('username')
    return redirect(url_for('admin.adminLogin'))

@admin.route('/index/<username>')
def adminIndex(username):
    adminLoginConfirm(username)

    pass

    return render_template('adminIndex.html', username=username)

