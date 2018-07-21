# -*- coding: utf-8 -*-
from wxpy import *
import json
from flask import Flask,request,send_file,url_for,make_response
import MsgHandler
import time
from WechatClient import WechatClient
import base64
from DataBase import DateBase

app=Flask(__name__)
robots={}

def init():
    # DataBase.connect()
    pass

def start():
    global app
    with app.test_request_context():
        url_for('static', filename='index.html')
    app.run(host='0.0.0.0')

def onLogOut(robot):
    global robots
    for key,value in robots.items():
        if value==robot:
            del robots[key]
    

# @app.route("/")
# def indexPage():
#     return send_file('index.html')

@app.route("/static/login",methods=['POST'])
def loginResponse():
    # global cursor,database
    db=DateBase()
    user=request.form.get('user')
    passwd=request.form.get('passwd')
    salt=request.form.get('salt')

    print user,' ',passwd
    if user is None or passwd is None or salt is None:
        return 'Bad request'
    if not db.secureCheck([user,passwd]):
        return 'Bad request'
    # if DataBase.search(user,passwd) is None:
    #     return 'no account or password incorrect'
    if not db.login(user,passwd,salt):
        db.close()
        return 'no account or password incorrect'
    access=db.updateAccess(user,passwd)
    resp=make_response('success')
    resp.set_cookie('robot_user',user,time.time())
    resp.set_cookie('robot_access',access,time.time())
    db.close()
    return resp

@app.route("/static/StartRobot",methods=['POST','GET'])
def startRobotResponse():
    global robots
    db=DateBase()
    access=request.cookies.get('robot_access')
    user=request.cookies.get('robot_user')
    if access is None:
        return 'Bad request'
    elif not db.checkAccess(user,access):
        db.close()
        return 'Bad request'
    elif user in robots.keys():
        db.close()
        return 'started'
    else:
        robots[user]=WechatClient('static/QRCode_%s.png'%user)
        robots[user].start()
        robots[user].logOutCallBackFunc=onLogOut
        db.close()
        return 'starting'

@app.route("/static/RobotCommand",methods=['GET'])
def robotCommandResponse():
    global robots
    db=DateBase()
    access=request.cookies.get('robot_access')
    user=request.cookies.get('robot_user')
    command=request.args['command']
    if access is None or command is None or user not in robots.keys():
        db.close()
        return 'Bad request'
    elif not db.checkAccess(user,access):
        db.close()
        return 'Bad request'

    robot=robots[user]
    if command=='GetState':
        db.close()
        return robot.getState(user)
    elif command=='GetList':
        friendList=robot.getList()
        his=db.getListenedHis(user)
        for chat in friendList['group']+friendList['friend']:
            if chat['name'].decode('utf-8') in his:
                chat['checked']=True
        db.close()
        return json.dumps(friendList)
    elif command=='Listen':
        value=request.args['value']
        robot.listen(value)
        res={'state':'success','listen':robot.targetListened_Name}
        db.updateListenedHis(user,json.dumps(robot.targetListened_Name,encoding='utf-8',ensure_ascii=False))
        db.close()
        return json.dumps(res,encoding='utf-8',ensure_ascii=False)
    elif command=='GroupMsg':
        msg=base64.b64decode(request.args['msg'])
        # msg=msg.decode('gb2312',errors='ignore')
        # msg=unicode(msg)
        msg=msg.decode('utf-8',errors='ignore')
        for chat in robot.targetListened_Obj:#这里如果列表包括自己微信号，会报错，所以直接暴力try
            try:
                chat.send_msg(msg)
                pass
            except:
                pass
        db.close()
        return 'success'
    elif command=='Stop':
        robot.stop()
        db.close()
        return 'success'
    elif command=='Exit':
        robot.exit()
        del robots[user]
        db.close()
        return 'success'
    else:
        db.close()
        return 'Bad request'




if __name__ == '__main__':
    MsgHandler.init()
    init()
    start()