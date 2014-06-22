#coding:utf-8
'''
Created on 2014年6月04日

@author: daT dev.tao@gmail.com
'''
import random


def music():
    musicList = [
                [r'http://up.yuedisk.com/wl/url/FPiPAabCCl/209595/yuedisk.mp3',r'好想大声说爱你',r'好想大声说爱你']             
                ]
    music = random.choice(musicList)
    musciUrl=music[0]
    musicTitle=music[1]
    musicDesc=music[2]
    
    return musciUrl,musicTitle,musicDesc