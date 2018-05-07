# -*- coding: utf-8 -*-
from wxpy import *
import RandomExpression
import DouTuLa
import Turing

def handle(msg):
    if msg.type==TEXT:
        print msg.sender,'>>>',msg.text
        #print type(msg.text)
        res=Turing.GetResponse(msg.text)
        print msg.sender,'<<<',res
        msg.reply_msg(u'「AI」'+res)
    elif msg.type==PICTURE:
        print msg.sender,'>>>收到表情'
        msg.get_file('temp/imgSave')
        imgUrl=DouTuLa.GetResponse('temp/imgSave')
        if imgUrl ==None:
            imgPath=RandomExpression.GetRandomExp()
        else:
            imgPath=DouTuLa.GetImage(imgUrl)
        msg.reply_image(imgPath)
        print msg.sender,'<<<回复表情',imgPath
    elif msg.type==RECORDING:
        pass
