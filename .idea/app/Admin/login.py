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
        name = form.name.data
        password = form.password.data

        admin = Admin.query.filter_by(name=name)
        if admin.count() == 0:
            flash('用户不存在')

        else:
            # print(admin.first().checkPassword(password))
            if admin.first().checkPassword(password):
                session['username'] = name
                return redirect(url_for('admin.adminIndex', name=name))
            else:
                flash('密码错误')

    return render_template('adminLogin.html', form=form)

@admin.route('/logout/<name>', methods=['GET'])
def adminLogout(name):
    # 身份验证
    adminLoginConfirm(name)
    session.pop('username')
    return redirect(url_for('admin.adminLogin'))



