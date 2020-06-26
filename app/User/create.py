
from app.User import user,jsonify,request,current_app,random_filename,User,db,os


@user.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        repeatpd = request.form.get('repeatpd')
        avatar = request.files.get('avatar')
        email = request.form.get('email')
        if password == repeatpd:
            user = User(
                name=name,
                password=password,
                email=email
            )
            db.session.add(user)
            db.session.commit()
            if avatar and avatar.filename != '':
                avatar.filename = random_filename('user' + str(user.id) + os.path.splitext(avatar.filename)[1])
                avatar.save(os.path.join(current_app.config['UPLOAD_PATH'], avatar.filename))
                user.avatar = avatar.filename
            db.session.commit()
            return jsonify({'event': 'success'})
        return jsonify({'error': 'password error'})
    return jsonify({'error': 'method error'})

