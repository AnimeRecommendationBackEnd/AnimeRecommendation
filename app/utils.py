import os
import uuid
import requests
import json

# 完结动画
url1 = "https://api.bilibili.com/x/web-interface/dynamic/region?ps=1000&rid=32"

def random_filename(filename):
    extension = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + extension
    return new_filename

def random_redis_token():
    token = uuid.uuid4().hex
    return token

def getMsg(url):
    datas = []
    data = requests.get(url)
    data = json.loads(data.text)
    try:
        for msg in data['data']['archives']:
            temp = {
                'picture': msg['pic'],
                'title': msg['title'],
                'introduce': msg['desc'],
                'bvid': msg['bvid'],
                'createtime': str(msg['ctime'])
            }
            datas.append(temp)
    except:
        pass
    return datas