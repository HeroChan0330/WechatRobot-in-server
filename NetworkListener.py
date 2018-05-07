# -*- coding: utf-8 -*-
from wxpy import *
import json
from flask import Flask,request
import MsgHandler
import sys
import thread 
import os

port='5000'
app = Flask('app')
targetRegistered=[]
frientList=''
friends_groups=[]
mRobot=None

hasQRCode=False
logined=False

def loginedCallback(robot):
    global frientList,friends_groups,mRobot,logined
    mRobot=robot
    friends_groups=mRobot.friends()+mRobot.groups()
    res_dict={"friend":[],"group":[]}
    index=0
    for friend in mRobot.friends():
        temp={'index':index,'name':friend.name.encode('utf-8')}
        #print friend.name.encode('utf-8')
        res_dict['friend'].append(temp)
        index+=1
    #index=0
    for group in mRobot.groups():
        temp={'index':index,'name':group.name.encode('utf-8')}
        res_dict['group'].append(temp)
        index+=1
    #print json.dumps(res_dict,encoding='utf-8',ensure_ascii=False)
    #print type(res_dict['friend'][0]['name'])
    #print json.dumps(res_dict,encoding='utf-8',ensure_ascii=False)
    # with open('list.txt','w') as fp:
    #     json.dump(res_dict,fp,encoding='utf-8')
    frientList=json.dumps(res_dict,encoding='utf-8',ensure_ascii=False)
    logined=True
    pass

def init():
    global app,port
    if len(sys.argv)>1:
        port=(sys.argv[1])
    app.run(port=int(port))
    
    

@app.route('/Command')
def response():
    global mRobot,friends_groups,targetRegistered,hasQRCode,app,port
    command=request.args.get('command')
    value=request.args.get('value')
    if command=='stop':
        targetRegistered=[]
        pass
    elif command=='listen':
        if not logined:
            return 'unlogined'
        #mRobot.registered.clear()
        #mRobot.registered.disable()
        targetIndex=value.split('|')
        targetRegistered=[]
        names=[]
        for index in targetIndex:
            target=friends_groups[int(index)]
            names.append(target.name)
            #mRobot.registered.append(target)
            targetRegistered.append(target)
        print targetRegistered
        return 'success listen'+json.dumps(names,ensure_ascii=False)
        pass
    elif command=='start':
        if not logined:
            return 'unlogined'
        return 'success'
        pass
    elif command=='getList':
        if not logined:
            return 'unlogined'
        return frientList
        pass
    elif command=='getState':
        if logined:
            listening=[]
            for target in targetRegistered:
                listening.append(target.name)
            res={'logined':'1','name':friends_groups[0].name,'listening':listening}
            return json.dumps(res,ensure_ascii=False)
        elif hasQRCode:
            res={'logined':'0','hasQRCode':'1','QRCodePath':'server/WechatQRCode_%s.png'%port}
            return json.dumps(res,ensure_ascii=False)
        else:
            res={'logined':'0','hasQRCode':'0'}
            return json.dumps(res,ensure_ascii=False)
    elif command=='exit':
        # if not logined:
        #     res={'logined':'0'}
        #     return json.dumps(res,ensure_ascii=False)
        #mRobot.stop()
        os.remove('wechatcache_%s.wxl'%port)
        os._exit(0)
    else:
        return 'bad request'
    pass

if __name__ == '__main__':
    init()