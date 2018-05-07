# -*- coding: utf-8 -*-
from wxpy import *
import json

from flask import Flask


frientList=''
app = Flask('app')

@app.route('/GetFrientList')
def response():
    return frientList

def startListen(robot):
    global frientList,app
    res_dict={"friend":[],"group":[]}
    #robot = Bot(cache_path='wechatcache.wxl')
    index=0
    for friend in robot.friends():
        temp={'index':index,'name':friend.name.encode('utf-8')}
        #print friend.name.encode('utf-8')
        res_dict['friend'].append(temp)
        index+=1
    index=0
    for group in robot.groups():
        temp={'index':index,'name':group.name.encode('utf-8')}
        res_dict['group'].append(temp)
        index+=1
    #print type(res_dict['friend'][0]['name'])
    #print json.dumps(res_dict,encoding='utf-8',ensure_ascii=False)
    # with open('list.txt','w') as fp:
    #     json.dump(res_dict,fp,encoding='utf-8')
    frientList=json.dumps(res_dict,encoding='utf-8',ensure_ascii=False)
    app.run()

if __name__ == '__main__':
    startListen(Bot(cache_path='wechatcache.wxl'))
    app.run()