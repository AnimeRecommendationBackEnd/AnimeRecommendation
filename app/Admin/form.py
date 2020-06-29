from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired

class adminLoginForm(FlaskForm):
    name = StringField(
        label=u'账号',
        validators=[
            DataRequired(u"请输入用户名")
        ],
        render_kw={
            "placeholder": "请输入用户名",
            "required": False
        }
    )
    password = PasswordField(
        label=u'密码',
        validators=[
            DataRequired(u"请输入密码")
        ],
        render_kw={
            "placeholder": "请输入密码",
            "required": False
        }
    )
    submit = SubmitField(u'登录')