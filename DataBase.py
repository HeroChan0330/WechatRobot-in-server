# -*- coding: utf-8 -*-
#required
import MySQLdb
import hashlib
import time
import json

cursor=None
database=None

sql_keywords=["\"","'",";","-","+",","]

def secureCheck(inputs):#if the context inputed contains the keyword,return false
    global sql_keywords
    for item in inputs:
        for kw in sql_keywords:
            if kw in item:
                return False
    return True

def connect():
    global cursor,database
    sqlUser='wechat_robot'
    sqlPw='H123456'
    sqlDB='wechat_robot'
    # 打开数据库连接
    database = MySQLdb.connect("localhost", sqlUser, sqlPw, sqlDB, charset='utf8' )
    # 使用cursor()方法获取操作游标
    cursor = database.cursor()

def search(user,passwd):
    global cursor,database
    query="select name,access from user where name='%s' AND passwd='%s';"%(user,passwd)
    cursor.execute(query)
    result=cursor.fetchall()
    if len(result)==0:
        return None
    return result[0]

def checkAccess(user,access):
    global cursor,database
    query="select name,access from user where name='%s' AND access='%s';"%(user,access)
    cursor.execute(query)
    result=cursor.fetchall()
    if len(result)==0:
        return False
    return True
    
def updateAccess(user,passwd):
    global cursor,database
    md5=hashlib.md5()
    md5.update('%s_%s_%d'%(user,passwd,time.time()))
    access=md5.hexdigest()
    #print access
    query="update user set access='%s' where name='%s';"%(access,user)
    #print query
    cursor.execute(query)
    database.commit()   
    return access

def updateListenedHis(user,his):
    global cursor,database
    query="update user set his='%s' where name='%s';"%(his,user)
    # print query
    cursor.execute(query)
    database.commit()

def getListenedHis(user):
    global cursor,database
    query="select name,his from user where name='%s';"%(user)
    cursor.execute(query)
    result=cursor.fetchall()
    if len(result)==0:
        return None
    res=json.loads(result[0][1],encoding='utf-8')
    return res


if __name__=='__main__':
    connect()
    # print search('HeroChan','123456')
    # print updateAccess('HeroChan','123456')
    #  print secureCheck(['Javons','HelloWorld'])
    updateListenedHis('HeroChan',json.dumps(["Hero Chan", "HeroChan"],encoding='utf-8',ensure_ascii=False))
