import os
import uuid
import requests
import json
import time

# 完结动画
animeMsgUrl = "https://api.bilibili.com/x/tag/info?tag_name="

def random_filename(filename):
    extension = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + extension
    return new_filename

def random_redis_token():
    token = uuid.uuid4().hex
    return token


animeType = {
    '10010': "原创",
    '10011': "漫画改",
    '10012': "小说改",
    '10013': "游戏改",
    '10014': "布袋戏",
    '10016': "热血",
    '10017': "穿越",
    '10018': "奇幻",
    '10020': "战斗",
    '10021': "搞笑",
    '10022': "日常",
    '10023': "科幻",
    '10024': "萌系",
    '10025': "治愈",
    '10026': "校园",
    '10027': "少儿",
    '10028': "泡面",
    '10029': "恋爱",
    '10030': "少女",
    '10031': "魔法",
    '10032': "冒险",
    '10033': "历史",
    '10034': "架空",
    '10035': "机战",
    '10036': "神魔",
    '10037': "声控",
    '10038': "运动",
    '10039': "励志",
    '10040': "音乐",
    '10041': "推理",
    '10042': "社团",
    '10043': "智斗",
    '10044': "催泪",
    '10045': "美食",
    '10046': "偶像",
    '10047': "乙女",
    '10048': "职场",
}

def getTypeAnime(type):
    url = "https://api.bilibili.com/pgc/season/index/result?season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&year=-1&style_id=%s&order=3&st=1&sort=0&page=1&season_type=1&pagesize=20&type=1" % type
    jsondata = requests.get(url).text
    datas = json.loads(jsondata)
    return datas

def makeData():
    datalist = []
    for key in animeType:
        print(key)
        datas = getTypeAnime(key)['data']['list']
        for data in datas:
            try:
                describe = json.loads(requests.get(animeMsgUrl + data['title']).text)['data']['content']
            except:
                describe = None
            temp = {
                'picture': data['cover'],
                'title': data['title'],
                'describe': describe,
                'link': data['link'],
                'isFinish': data['is_finish'],
                'seasonId': data['season_id'],
                'tag': animeType[key]
            }
            datalist.append(temp)
            time.sleep(10)
    return datalist


