# -*- coding: utf8 -*-
from wxpy import *
import RandomExpression
import DouTuLa
import MsgHandler
import NetworkListener
import thread
import requests
import os
import threading
import time

port='5000'

def qrCallback(uuid, status, qrcode):
    NetworkListener.hasQRCode=True
    with open('WechatQRCode_%s.png'%port,'wb') as fp:
        fp.write(qrcode)

def listener():
    NetworkListener.init()



try:
    if len(sys.argv)>1:
        port=(sys.argv[1])
    requests.get('http://127.0.0.1:%s/Command?command=getState'%port)
    print 'launched'
    os._exit(0)
except:
    print 'launching'


DouTuLa.Init()
serverThread= threading.Thread(target=listener,args=())
serverThread.setDaemon(True)
serverThread.start()
robot = Bot(cache_path='wechatcache_%s.wxl'%port,console_qr =False,qr_callback =qrCallback)
#robot = Bot(console_qr =False,qr_callback =qrCallback) #不保留cache
while robot is None:
    print robot
    time.sleep(1)
NetworkListener.loginedCallback(robot)

@robot.register(robot.friends()+robot.groups(),[TEXT,PICTURE])
def response(msg):
    #print NetworkListener.targetRegistered
    if msg.sender in NetworkListener.targetRegistered:
        MsgHandler.handle(msg)
    else:
        print '[Robot]receive msg,but the sender isn`t in the registered list'
        #MsgHandler.handle(msg)
embed()




