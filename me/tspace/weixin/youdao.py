#coding:utf-8
'''
Created on 2014年5月29日

@author: daT dev.tao@gmail.com
'''
import urllib2
import json


def youDao(word):
    """
    有道翻译，去有道申请key
    """
    qword = urllib2.quote(word)
    baseUrl = r'http://fanyi.youdao.com/openapi.do?keyfrom=tspace&key=864347886&type=data&doctype=json&version=1.1&q='
    
    url = baseUrl + qword
    resp = urllib2.urlopen(url)
    
    fanyi = json.loads(resp.read())
    #print fanyi
    if fanyi['errorCode'] == 0: 
        if 'basic' in fanyi.keys():
            trans = u'%s:\n%s\n%s\n网络释义：\n%s' %(fanyi['query'],' '.join(fanyi['translation']),' '.join(fanyi['basic']['explains']),' '.join(fanyi['web'][0]['value']))
            return trans
        else:
            return u'Sorry，您输入的单词超出我的理解范围，请搞一个简单些的来请教～～'
    if fanyi['errorCode'] == 20:
        return u'Sorry,要翻译的文本过长'
    if fanyi['errorCode']==30:
        return u'Sorry,无法进行有效的翻译'
    if fanyi['errorCode']==40:
        return u'Sorry,不支持的语言类型'
    else:
        return u'Sorry,无词典结果，仅在获取词典结果生效'





if __name__=="__main__":
    print youDao("hello")   ;