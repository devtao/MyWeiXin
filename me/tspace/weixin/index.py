#coding:utf-8
'''
Created on 2014年5月29日

@author: daT dev.tao@gmail.com
'''

import os 
import web
import hashlib
import time
from lxml import etree
from youdao import youDao
from music import music
import memcache
from xiaohuangji import xiaoHuangJi

urls=(
      '/Weixin','WeiXinInterface'
      )


app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root,'templates')
render = web.template.Render(templates_root)


mc=memcache.Client(['127.0.0.1:11211'],debug=0)


class WeiXinInterface:
    
    def __init__(self):
        print 'come in'
        #self.app_root = os.path.dirname(__file__)
        #self.templates_root = os.path.join(self.app_root,'templates')
        #self.render = web.template.Render(self.templates_root)
        
    
    def GET(self):
        print 'get'
        data = web.input()
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr
        token = 'liutao'
        list = [token,timestamp,nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update,list)
        hashcode = sha1.hexdigest()
        
        if hashcode == signature:
            return echostr
        
        
    def POST(self):        
        str_xml = web.data() #获得post来的数据
        xml = etree.fromstring(str_xml)#进行XML解析
        content=xml.find("Content").text#获得用户所输入的内容
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        
        
        #增加订阅与退订事件
        if msgType =='event':
            mscontent = xml.find("Event").text
            if mscontent =='subscribe':
                replyText = u'''  欢迎关注大T的微信平台，目前提供在线翻译，调戏小黄鸡智能聊天机器人，未来将有今日足彩推荐。输入help查看帮助命令'''                       
                return render.reply_text(fromUser,toUser,int(time.time()),replyText)
            if mscontent =='unsubscribe':
                replyText = u'''我目前功能还简单，在不断完善中，随时欢迎您回来！'''
                return render.reply_text(fromUser,toUser,int(time.time()),replyText)
            
        #增加help操作        
        if msgType =='text':

            if content == 'help':
                replyText = u'''**********************\n1.直接输入英文或者中文返回对应的中英翻译\n2.输入xhj你就可以调戏小贱鸡了\n3.今日足彩推荐\n******************   '''
                return render.reply_text(fromUser,toUser,int(time.time()),replyText)                   
        
            if content == 'music':
                musicUrl,musicTitle,musicDesc = music()
                print musicUrl
                print musicTitle
                print musicDesc
                return render.reply_music(fromUser,toUser,int(time.time()),musicUrl,musicTitle,musicDesc)
        
            if content.lower() == 'bye':
                mc.delete(fromUser+'_xhj')
                return render.reply_text(fromUser,toUser,int(time.time()),u'*******************\n您已经跳出了和小贱鸡的交谈中，输入help来显示操作指令\n*******************')
            
            if content.lower() == 'xhj':
                mc.set(fromUser+'_xhj','xhj')#set memcache
                return render.reply_text(fromUser,toUser,int(time.time()),u'********************\n您已经进入与小贱鸡的交谈中，随便搞吧骚年！输入bye跳出与小黄鸡的交谈\n*********************')
            
            mcxhj = mc.get(fromUser+'_xhj')#get memcache
            
            if mcxhj == 'xhj':
                reply = xiaoHuangJi(content)
                reply_text = reply['sentence_resp']
                return render.reply_text(fromUser,toUser,int(time.time()),reply_text)
            
            #翻译
            #如果是unicode则对其进行utf-8转码
            if type(content).__name__=="unicode":
                content = content.encode("utf-8")    
            res =youDao(content)
            return render.reply_text(fromUser,toUser,int(time.time()),res)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

