# -*- coding: utf-8 -*-
#required
import MySQLdb
import hashlib
import time

cursor=None
database=None

sql_keywords=["\"","'","and","exec","insert","select","delete","update","count","*","%","chr","mid","master","truncate","char","declare",";","or","-","+",","]

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

if __name__=='__main__':
    connect()
    print search('HeroChan','123456')
    print updateAccess('HeroChan','123456')