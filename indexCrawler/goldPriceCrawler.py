#encoding:utf8
'''
本程序源码包括了黄金等主要指数的历史行情数据抓取工作
'''
__author__ = 'xuyuming'
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'   #解决ORACLE插入中文乱码问题
from urllib import urlopen
import time
from bs4 import BeautifulSoup
from sqlalchemy import *
from sqlalchemy.dialects.oracle import \
            BFILE, BLOB, CHAR, CLOB, DATE, \
            DOUBLE_PRECISION, FLOAT, INTERVAL, LONG, NCLOB, \
            NUMBER, NVARCHAR, NVARCHAR2, RAW, TIMESTAMP, VARCHAR, \
            VARCHAR2  #引入ORACLE专用字符集
from sqlalchemy.sql import select
from sqlalchemy.sql import text #用于导入自定义文本SQL
from sqlalchemy.schema import *
import pandas as pd
import tushare as ts
import re
from model import goldHistoricalData,engine
from selenium import webdriver
import time
import datetime
def rgxDateConvert(dateStr):
    '''
    将 ****年**月**日的字符串格式转化成日期格式数据
    :param dateStr:
    :return:
    '''
    m=re.match(u'(\d+)年(\d+)月(\d+)日',dateStr)
    s=m.group(1)+'-'+m.group(2)+'-'+m.group(3)
    tm=time.strptime(s,'%Y-%m-%d')
    y,m,d=tm[0:3]
    print datetime.datetime(y,m,d)


def readHistoricalData():
    '''
    读取日线行情数据,包括多品种信息
    :return:
    '''
    df = pd.read_csv(u"黄金.csv",skiprows=0)
    df['tradeday']=pd.to_datetime(df['tradeday'])#将字符串类型的交易日期转换成日期
    df['type']='gold'
    conn=engine.connect()
    df.to_sql('daylyquote',engine,if_exists='replace',index=False)
    conn.close()
def detailPageCrawler():
    '''
    http://www.sge.com.cn/xqzx/mrxq/index_%s.shtml
    其中%s代表了页数，http://www.sge.com.cn/xqzx/mrxq/index.shtml是第一页

    :return:
    '''
    driver=webdriver.PhantomJS(executable_path=r'C:\Users\xuyuming\AppData\Roaming\Python\Scripts\phantomjs')
    driver.get('http://cn.investing.com/commodities/gold-historical-data')
    #1,取首页的明细页列表，同时记录一共有多少页分页
    time.sleep(1)
    quotes=driver.find_elements_by_xpath('//*[@id="curr_table"]/tbody/tr[1]/td')
    newQuote={'tradeday':rgxDateConvert(quotes[0].text),
           'closeprice':quotes[0].text,
           'open':quotes[1].text,
           'high':quotes[2].text,
           'low':quotes[3].text,
           'vol':quotes[4].text,
           'change':quotes[5].text}
    print newQuote


    # #2,从分页第二页开始，依次记录每一页的当中出现详细行情页列表，加入到页面列表当中
    # detailPageList=[]
    # templist=soup.select("#zl_list > li > a")
    # for i in templist:
    #     detailPageList.append(i.get('href'))
    # pagecount=2
    # while(true):
    #     textdata=urlopen('http://www.sge.com.cn/xqzx/mrxq/index_%s.shtml'%(pagecount)).read()
    #     soup=BeautifulSoup(textdata,'lxml')
    #     templist=soup.select("#zl_list > li > a")
    #     if len(templist)==0:
    #         break
    #     for i in templist:
    #         detailPageList.append(i.get('href'))
    #     pagecount+=1
    # return detailPageList

###############下需进入主函数#########################
####1，抓取历史数据################
detailPageCrawler()
####2，每天处理增量数据################
