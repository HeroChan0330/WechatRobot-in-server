# -*- coding: utf8 -*-
import requests
import json

#这里需要自行添加key 和id


def GetResponse(msg):
    response=requests.post("http://www.tuling123.com/openapi/api",{"info":msg,"key":"","userid":""})
    response.encoding='utf8'
    #print response.text
    res=json.loads(response.text)
    return res['text']

def GetResponse2(msg):
    content={"perception": {"inputText": {"text": msg}},"userInfo": {"apiKey": "","userId": ""}}
    response=requests.post("http://openapi.tuling123.com/openapi/api/v2",str(content))
    response.encoding='utf8'
    #print response.text
    res=json.loads(response.text)
    return res['results'][0]['values']['text']

if __name__=="__main__":
    print GetResponse("怎么了？")