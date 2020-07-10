from flask import Blueprint,jsonify,request,current_app,session,send_from_directory
from app.models import *
from app.utils import *
from app.extensions import *
import os


user = Blueprint('user', __name__)

url = {
    "/user/create":{
        'POST':{
        'name':'true',
        'password':'true',
        'repeatpd':'true',
        'avatar':'false',
        'email':'true'
        }
    },
    '/user/login':{
        'POST':{
        'name':'true',
        'password':'true'
        }
    },
    '/user/logout':{
        'POST':{
        'token':'true'
        }
    },
    '/user/updata':{
        'POST':{
        'token':'true',
        'name':'false',
        'password':'false',
        'avatar':'false',
        'email':'false'
        }
    },
    '/user/search':{
        'POST':{
        'email':'false'
        }
    },
    '/user/follows':{
        'POST':{
        'token':'true',
        'userid':'true'
        },
        'DELETE':{
        'token': 'true',
        'userid': 'true'
        }
    },
    '/user/get':{
        'GET':{
        'page':'false',
        'userid':'false',
        'ask':'false'
        }
    },
    '/user/recommend':{
        'POST':{
        'token':'true',
        'title':'true',
        'content':'true',
        'animetitle':'true',
        'describe':'true',
        'datafrom':'false',
        'link':'false',
        'seasonid':'false',
        'tag1':'false',
        'tag2':'false',
        'tag3':'false'
        },
        'DELETE':{
        'token':'true',
        'dramaid':'true'
        }
    },
    '/user/recommend/comment':{
        'POST':{
        'token':'true',
        'content':'true',
        'dramaid':'true',
        'reply':'false',
        'commentid':'false'
        },
        'DELETE':{
        'token':'true',
        'commentid':'true'
        }
    },
    '/user/recommend/star':{
        'POST':{
        'token':'true',
        'dramaid':'true'
        },
        'DELETE':{
        'token':'true',
        'dramaid':'true'
        }
    },
    '/user/recommend/collect':{
        'POST':{
        'token': 'true',
        'dramaid': 'true'
        },
        'DELETE':{
        'token': 'true',
        'dramaid': 'true'
        }
    },
    '/user/recommend/get':{
        'GET':{
        'page':'false',
        'dramaid':'false',
        'ask':'false'
        }
    },
    '/user/ask':{
        'POST':{
        'token':'true',
        'title':'true',
        'content':'true'
        },
        'DELETE':{
        'token':'true',
        'dramaid':'true'
        }
    },
    '/user/ask/solve':{
        'POST':{
            'token':'true',
            'dramaid':'true'
        },
        'DELETE':{
            'token':'true',
            'dramaid':'true'
        }
    },
    '/user/ask/get':{
        'GET':{
            'page': 'false',
            'dramaid': 'false',
            'ask': 'false'
        }
    },
    '/user/person':{
        'GET':{
            'token':'true'
        }
    },
    '/user/person/fans':{
        'GET':{
            'token':'true',
            'userid':'false'
        }
    },
    '/user/person/follower': {
        'GET': {
            'token': 'true',
            'userid':'false'
        }
    },
    '/user/person/recommend': {
        'GET': {
            'token': 'true',
            'userid':'false'
        }
    },
    '/user/person/ask': {
        'GET': {
            'token': 'true',
            'userid':'false'
        }
    }
}

@user.before_request
def method_verify():
    key_train = set(url[str(request.url_rule)][request.method].keys())
    key_test = set(request.form)
    key_error = key_test.difference(key_train)
    key_true = key_train.difference(key_test)
    key_need = []
    for key in key_true:
        if url[str(request.url_rule)][request.method][key] == 'true':
            key_need.append(key)
    if key_need and key_error:
        return jsonify(Event1005('缺少了必须的参数'+str(key_need)+',传入了多余的参数'+str(key_error)))
    elif key_need:
        return jsonify(Event1005('缺少了必须的参数' + str(key_need)))
    elif key_error:
        return jsonify(Event1005('传入了多余的参数' + str(key_error)))


import app.User.create
import app.User.login
import app.User.updata
import app.User.show


