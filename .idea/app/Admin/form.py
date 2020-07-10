from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, FileField
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


class finishedAnimeForm(FlaskForm):
    bvid = StringField(
        label=u'bvid',
        validators=[
            DataRequired(u"请输入bvid")
        ],
        render_kw={
            "placeholder": "请输入bvid",
            "required": False
        }
    )
    title = StringField(
        label=u'标题',
        validators=[
            DataRequired(u"请输入标题")
        ],
        render_kw={
            "placeholder": "请输入标题",
            "required": False
        }
    )
    introduce = StringField(
        label=u'介绍',
        validators=[
            DataRequired(u"请输入介绍")
        ],
        render_kw={
            "placeholder": "请输入介绍",
            "required": False
        }
    )
    picture = FileField(
        label=u'封面',
    )
    createtime = StringField(
        label=u'时间',
        validators=[
            DataRequired(u"请输入时间")
        ],
        render_kw={
            "placeholder": "请输入时间",
            "required": False
        }
    )
    submit = SubmitField(u'提交')