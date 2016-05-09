#coding=utf-8
__author__ = 'xuyuming'
from urllib import urlopen
import time
from bs4 import BeautifulSoup
textdata=urlopen('http://sh.lianjia.com/chengjiao/d1000').read()#取官方网站当中保证金余额变动数据
soup=BeautifulSoup(textdata,'lxml')
# print soup
# body > div.wrapper > div.main-box.clear > div > div.list-wrap > ul > li:nth-child(1) > div.info-panel > h2 > a
# 摸拟登录
# 首先启动一个循环，确保每一笔成交都能抓到
basicinfos=soup.select('body > div.wrapper > div.main-box.clear > div > div.list-wrap > ul > li > div.info-panel > h2 > a')
quxians=soup.select('body > div.wrapper > div.main-box.clear > div > div.list-wrap > ul > li > div.info-panel > div > div.col-1.fl > div.other > div ')
qianyueriqis=soup.select('body > div.wrapper > div.main-box.clear > div > div.list-wrap > ul > li > div.info-panel > div > div.col-2.fr > div > div:nth-of-type(1) > div')
qianyuedanjias=soup.select()
qianyuezongjia=soup.select()
for quxian in quxians:
    print list((quxian.stripped_strings))[0],list((quxian.stripped_strings))[1],list((quxian.stripped_strings))[3].split(r'/')[0],list((quxian.stripped_strings))[3].split(r'/')[1],\
    list((quxian.stripped_strings))[5]
for qianyueriqi in qianyueriqis:
    print qianyueriqi.get_text()

# 筛选所需信息
for basicinfo in basicinfos:
    xiaoqumingchen=basicinfo.get_text().split(' ')[0]
    id=basicinfo.get('key')
    huxing=basicinfo.get_text().split(' ')[1]
    mianji= basicinfo.get_text().split(' ')[2]
    print id,xiaoqumingchen,huxing,mianji

#body > div.wrapper > div.main-box.clear > div > div.list-wrap > ul > li:nth-child(1) > div.info-panel > div > div.col-1.fl > div.other > div > a:nth-child(1)

