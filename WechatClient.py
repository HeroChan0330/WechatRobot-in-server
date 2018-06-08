# -*- coding: utf-8 -*-
from wxpy import *
import MsgHandler
import json
import thread
import threading

class WechatClient:
    hasQRCode=False#是否获得登录二维码
    logined=False#是否已登录
    qrCodePath=''
    robot=None
    cachePath=None
    consoleQR=False
    targetListened_Obj=[]#被监听的对象
    targetListened_Name=[]#被监听的对象昵称
    friends_groups=[]
    friendList_JsonStr=''
    friendList=[]
    
    logOutCallBackFunc=None

    def __init__(self,qrCodePath):
        self.qrCodePath=qrCodePath

    def robotInit(self,threadName, delay):
        threadLock = threading.Lock()
        threadLock.acquire()
        self.robot=Bot(cache_path=self.cachePath,console_qr=self.consoleQR,qr_callback=self.qrCallback,logout_callback=self.logoutCallback)
        self.loginCallback()
        #艹这里等待输入的时候堵塞线程了。。。。
        #TODO:用另外一个线程执行这个等待操作，或者找找有没有回调函数不堵塞线程
        # self.friends_groups=self.robot.friends()+self.robot.groups()
        self.robot.register(self.robot.friends()+self.robot.groups(),[TEXT,PICTURE])(self.response)
        threadLock.release()
    
    def start(self):
        thread.start_new_thread( self.robotInit, ("InitThread", 2, ) )
        #self.robot=Bot(cache_path=self.cachePath,console_qr=self.consoleQR,qr_callback=self.qrCallback)
        #self.loginCallback()
        # 艹这里等待输入的时候堵塞线程了。。。。
        # TODO:用另外一个线程执行这个等待操作，或者找找有没有回调函数不堵塞线程
        # self.friends_groups=self.robot.friends()+self.robot.groups()
        pass

    def response(self,msg):
        print msg
        if msg.sender in self.targetListened_Obj:
            MsgHandler.handle(msg)
        else:
            print '[Robot]receive msg,but the sender isn`t in the registered list'

        
    def qrCallback(self,uuid, status, qrcode):
        self.hasQRCode=True
        with open(self.qrCodePath,'wb') as fp:
            fp.write(qrcode)

    def loginCallback(self):
        print self.robot
        res_dict={"friend":[],"group":[]}
        index=0
        for friend in self.robot.friends():
            temp={'index':index,'name':friend.name.encode('utf-8'),'checked':False}
            #print friend.name.encode('utf-8')
            res_dict['friend'].append(temp)
            index+=1
        #index=0
        for group in self.robot.groups():
            temp={'index':index,'name':group.name.encode('utf-8'),'checked':False}
            res_dict['group'].append(temp)
            index+=1
        self.friendList_JsonStr=json.dumps(res_dict,encoding='utf-8',ensure_ascii=False)
        self.friendList=res_dict
        self.friends_groups=self.robot.friends()+self.robot.groups()
        self.logined=True

    def listen(self,indexs):
        targetIndex=indexs.split('|')
        self.targetListened_Obj=[]
        self.targetListened_Name=[]
        for index in targetIndex:
            target=self.friends_groups[int(index)]
            self.targetListened_Name.append(target.name)
            self.targetListened_Obj.append(target)
        print self.targetListened_Obj
    
    def stop(self):
        self.targetListened_Obj=[]
        self.targetListened_Name=[]

    def exit(self):
        # self.robot.stop()
        self.stop()
        self.logined=False
        self.hasQRCode=False
        self.robot.logout()

    def getState(self,access):
        if self.logined:
            res={'logined':'1','name':self.friends_groups[0].name,'listening':self.targetListened_Name}
            return json.dumps(res,ensure_ascii=False)
        elif self.hasQRCode:
            res={'logined':'0','hasQRCode':'1','QRCodePath':'QRCode_%s.png'%access}
            return json.dumps(res,ensure_ascii=False)
        else:
            res={'logined':'0','hasQRCode':'0'}
            return json.dumps(res,ensure_ascii=False)

    def getList(self):
        # return self.friendList_JsonStr
        return self.friendList

    def logoutCallback(self):
        print 'Log Out!!!'
        if self.logOutCallBackFunc is not None:
            self.logOutCallBackFunc(self)
            self.exit()
    
if __name__=='__main__':
    wechatClient=WechatClient('1.png')
    wechatClient.start()
    embed()