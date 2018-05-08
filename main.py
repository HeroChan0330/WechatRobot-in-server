# -*- coding: utf8 -*-
from wxpy import *
import DouTuLa
import MsgHandler
import NetworkListener

if __name__=='__main__':
    MsgHandler.init()
    NetworkListener.init()
    NetworkListener.start()