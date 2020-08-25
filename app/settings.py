import os

# MySQL数据库连接
#SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/data?charset=utf8"
SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1:3306/data?charset=utf8"

# 数据库追踪关闭
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 密钥设置
SECRET_KEY = "SecretKey"

# JSON自动排序关闭
JSON_SORT_KEYS = False

#文件下载地址
UPLOAD_PATH = os.path.join(os.path.join(os.path.dirname(__file__),'uploads'))

#邮箱发信服务器
MAIL_SERVER = 'smtp.qq.com'

MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_PORT = 465

'''#邮箱发信端口
MAIL_POST = 587

#邮箱使用SSL/TLS
MAIL_USE_TLS = True'''

#邮箱地址
MAIL_USERNAME = '1193299044@qq.com'

#邮箱授权码
MAIL_PASSWORD = 'tmromcasvenvhgba'

#默认发信人
MAIL_DEFAULT_SENDER = '通信人<1193299044@qq.com>'

#whooshee最小搜索字数
WHOOSHEE_MIN_STRING_LEN = 1
