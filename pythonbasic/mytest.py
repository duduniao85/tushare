#coding=utf-8
__author__ = 'xuyuming'
import tushare as ts

from urllib import urlopen
from bs4 import BeautifulSoup
from sqlalchemy import *
from sqlalchemy.types import (BigInteger, Integer, Float, Text, Boolean,
            DateTime, Date, Time, NVARCHAR, String ,CHAR)
from sqlalchemy.sql import select
from sqlalchemy.schema import *
import tushare as ts
import re
# ts.get_h_data(code='399106',index=True,end='2016-03-31')
# print ts.get_h_data(code='000001',start='2013-01-01',index=True,autype=None)
# df=ts.get_today_all()#一次性获取最近一个日交易日所有股票的交易数据
# print df
# print df['nmc'].sum()
# #总流通市值
# print df['volume'].sum()#总成交金额
#将日期与交易日进行判断，如果日期为交易日，则启动将总流通市值和成交金额自动落地的程序,连同其它数据一起落地，利用APScheduler完成定时任务的启动

####################################获取沪市A股数据#####################
# mt = ts.Master()
# df = mt.TradeCal(exchangeCD='XSHG', beginDate='20150928', endDate='20151010', field='calendarDate,isOpen,prevTradeDate')
text=urlopen('http://www.sse.com.cn/market/stockdata/overview/day/').read()#取官方网站当中保证金余额变动数据
print text
#取最新的沪市A股数据日期
m= re.search(r'searchDate\ \=\ \'([0-9]+\-[0-9]+\-[0-9]+)\'',text)
searchDate=m.group(1)
#取最新的沪市A股流通市值
m= re.search(r'negotiableValueA\ \=\ \'([0-9]+\.[0-9]+)\'',text)
negotiableValueA_sh=m.group(1)
#取最新的沪市A股成交金额
m= re.search(r'trdAmtA\ \=\ \'([0-9]+\.[0-9]+)\'',text)
trdAmtA_sh=m.group(1)
#取最新的沪市A股平均市盈率
m= re.search(r'profitRateA\ \=\ \'([0-9]+\.[0-9]+)\'',text)
profitRateA_sh=m.group(1)
print negotiableValueA_sh,trdAmtA_sh,profitRateA_sh,searchDate



####################################获取深市A股数据#####################
text=urlopen('http://www.szse.cn/main/marketdata/tjsj/jyjg/').read()
soup=BeautifulSoup(text)
#取数据日期
for tabb in  soup.findAll('span',class_='cls-subtitle')[0:1]:
     searchdate_sz=tabb.string
     print searchdate_sz
for tabb in  soup.findAll('tr',class_='cls-data-tr')[0:1]:
     total_tradeamt=tabb.findAll('td')[2].string #股票总成交金额
     print total_tradeamt
     negotiableValue=tabb.findAll('td')[7].string #股票总流通市值
     print negotiableValue
for tabb in  soup.findAll('tr',class_='cls-data-tr')[2:3]:
     tradeamtB=tabb.findAll('td')[2].string #b股总成交金额
     print tradeamtB
     negotiableValueB=tabb.findAll('td')[7].string #b股总流通市值
     print negotiableValueB
negotiableValueA_sz=int(negotiableValue.replace(',',''))-int(negotiableValueB.replace(',',''))   # 深市A股总流通市值为深市总市值减去深市B股总市值
tradeamtA_sz=int(total_tradeamt.replace(',',''))-int(tradeamtB.replace(',','')) # 深市A股总成交额为深市总成交额减去深市B股总成交额
print negotiableValueA_sz,tradeamtA_sz

#两市加总
total_tradeamtA=tradeamtA_sz+float(trdAmtA_sh)*100000000 #沪市单位为亿
total_negotiableValueA=negotiableValueA_sz+float(negotiableValueA_sh)*100000000 #沪市单位为亿



