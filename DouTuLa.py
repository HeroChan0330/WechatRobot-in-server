#-*- coding:utf8 -*-
import random
import requests
import json
import BaiduOCR
import RandomExpression
import urllib

def init():
    BaiduOCR.GetToken()

def GetResponse_Kw(keyword):
    url='https://www.doutula.com/api/search?keyword=%s&mime=0&page=0'%urllib.quote(keyword)
    reqHeaders={
        'user-agent': 'Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46',
        'pragma': 'no-cache',
        'upgrade-insecure-requests': '1'
    }
    req=requests.get(url,headers=reqHeaders)
    # req.encoding='gbk'
    # print(url)
    # print(req.text)
    reqJson=json.loads(req.text,encoding='utf-8')
    cnt=len(reqJson['data']['list'])
    index=int(random.uniform(0,cnt))
    return reqJson['data']['list'][index]['image_url']

def GetResponse(imagePath):
    kw=BaiduOCR.BaiduOCR(imagePath)
    if len(kw)==0:
        return None
    return GetResponse_Kw(kw)

def GetResponse_Stream(stream):
    kw=BaiduOCR.BaiduOCR_Stream(stream)
    return GetResponse_Kw(kw)

def GetImage(url):
    content=requests.get(url)
    fileName='temp/'+url[url.rindex('/')+1:]
    fp=open(fileName,'wb')
    fp.write(content.content)
    fp.close()
    return fileName

if __name__=='__main__':
    BaiduOCR.GetToken()
    imgUrl=GetResponse('temp/imgSave')
    if imgUrl ==None:
        imgPath=RandomExpression.GetRandomExp()
    else:
        imgPath=GetImage(imgUrl)
    print imgPath