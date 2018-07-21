# -*- coding: utf-8 -*-
#required
import MySQLdb
import hashlib
import time
import json

class DateBase:
    cursor=None
    database=None
    sql_keywords=["\"","'",";","-","+",","]

    def __init__(self):
        self.connect()


    def secureCheck(self,inputs):#if the context inputed contains the keyword,return false
        for item in inputs:
            for kw in self.sql_keywords:
                if kw in item:
                    return False
        return True

    def connect(self):
        sqlUser='wechat_robot'
        sqlPw='123456'
        sqlDB='wechat_robot'
        # 打开数据库连接
        self.database = MySQLdb.connect("localhost", sqlUser, sqlPw, sqlDB, charset='utf8' )
        # 使用cursor()方法获取操作游标
        self.cursor = self.database.cursor()

    def close(self):
        self.database.close()

    def login(self,user,passwd,salt):
        query="select name,passwd from user where name='%s';"%(user)
        self.cursor.execute(query)
        result=self.cursor.fetchall()
        if len(result)==0:
            return False
        key=user+result[0][1]+salt
        md5=hashlib.md5()
        md5.update(key)
        key=md5.hexdigest()
        if passwd==key:
            return True
        return False


    def search(self,user,passwd):
        query="select name,access from user where name='%s' AND passwd='%s';"%(user,passwd)
        self.cursor.execute(query)
        result=self.cursor.fetchall()
        if len(result)==0:
            return None
        return result[0]

    def checkAccess(self,user,access):
        query="select name,access from user where name='%s' AND access='%s';"%(user,access)
        self.cursor.execute(query)
        result=self.cursor.fetchall()
        if len(result)==0:
            return False
        return True
        
    def updateAccess(self,user,passwd):
        md5=hashlib.md5()
        md5.update('%s_%s_%d'%(user,passwd,time.time()))
        access=md5.hexdigest()
        #print access
        query="update user set access='%s' where name='%s';"%(access,user)
        #print query
        self.cursor.execute(query)
        self.database.commit()   
        return access

    def updateListenedHis(self,user,his):
        query="update user set his='%s' where name='%s';"%(his,user)
        # print query
        self.cursor.execute(query)
        self.database.commit()

    def getListenedHis(self,user):
        query="select name,his from user where name='%s';"%(user)
        self.cursor.execute(query)
        result=self.cursor.fetchall()
        if len(result)==0:
            return None
        res=json.loads(result[0][1],encoding='utf-8')
        return res


if __name__=='__main__':
    db=DateBase()
    print(db.getListenedHis("HeroChan"))
    db.close()
    # print search('HeroChan','123456')
    # print updateAccess('HeroChan','123456')
    #  print secureCheck(['Javons','HelloWorld'])
    # updateListenedHis('HeroChan',json.dumps(["Hero Chan", "HeroChan"],encoding='utf-8',ensure_ascii=False))
