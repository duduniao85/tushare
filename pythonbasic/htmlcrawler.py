#coding=utf-8
__author__ = 'xuyuming'
from urllib import urlopen
from bs4 import BeautifulSoup
from sqlalchemy import *
from sqlalchemy.types import (BigInteger, Integer, Float, Text, Boolean,
            DateTime, Date, Time, NVARCHAR, String ,CHAR)
from sqlalchemy.sql import select
from sqlalchemy.schema import *
import tushare as ts
import re
#开始取上次数据日期



df=ts.get_hist_data('sh',start='2010-01-01')#开始取上证指数增量日期当中的行情数据
text=urlopen('http://www.sipf.com.cn/subject/sub_ch/tjsj/index.html').read()#取官方网站当中保证金余额变动数据
soup=BeautifulSoup(text)
soup.prettify()#格式化HTML源文本
for tabb in  soup.findAll('table')[1:2]:
     tr_garanteebal=tabb.findAll('tr')[2]
     date=tr_garanteebal.findAll('p')[0].string #获取证券交易结算资金的日期时间段
     print date
     endvolume= tr_garanteebal.findAll('p')[2].string#获取证券交易结算资金的期末余额
     avgvolume=tr_garanteebal.findAll('p')[3].string#获取证券交易结算资金的平均余额
     involume=tr_garanteebal.findAll('p')[4].string#获取证券交易结算资金的转入额
     outvolume=tr_garanteebal.findAll('p')[5].string#获取证券交易结算资金的转出额
     tradeday=date[0:4]+'-'+date[11:13]+'-'+date[-2:]
     print tradeday
# print date[0:4]+date[11:13]+date[-2:]+' '+(int)(endvolume.replace(',',''))+' '+(int)(avgvolume.replace(',',''))+' '+(int)(involume.replace(',',''))+' '+(int)(outvolume.replace(',',''))
#接下来将定义一个函数，用于执行指定的SQL语句以及连接指定的数据库
db_engine=create_engine('oracle+cx_oracle://quant:1@127.0.0.1:1521/XE', echo=True)
meta=MetaData()
t = Table("guarantee_balance",meta, autoload=True, autoload_with=db_engine)
ins=t.insert().values(tradeday=tradeday,endvolume=int(endvolume.replace(',','')), avgvolume=int(avgvolume.replace(',','')), involume=int(involume.replace(',','')),outvolume=int(outvolume.replace(',','')))
conn=db_engine.connect()
s=select([t]).where(t.c.tradeday==tradeday)
result=conn.execute(s).fetchall() #取得所有结果集合LIST
print  type(result)
if len(result)==0:
     conn.execute(ins) #插入保证金余额表
df.to_sql('shangzhengzongzhi',db_engine,if_exists='replace',dtype={'date': CHAR(10)})#将历史的上证指数行情数据落到本地
conn.close()
######################################下面开始抓取每日A股流通市值数据和总成交金额，如果有一天存在漏抽，#######
# 则需要从上交所和深交所网站中提取相关数据补录################################################################
##############################################################################################################

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



####################################获取深市A股数据开始########################################
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

db_engine=create_engine('oracle+cx_oracle://quant:1@127.0.0.1:1521/XE', echo=True)
meta=MetaData()
t = Table("a_gu_stat",meta, autoload=True, autoload_with=db_engine)#连接指定的表名
ins=t.insert().values(tradeday=searchdate_sz,liutongshizhi=int(total_negotiableValueA), chengjiajine=int(total_tradeamtA))#生成插入语句对应的数据库对象
conn=db_engine.connect()
s=select([t]).where(t.c.tradeday==searchdate_sz)#查找是否该交易日已经有了对应的数据
result=conn.execute(s).fetchall() #取得所有结果集合LIST
print  type(result)
if len(result)==0:
     conn.execute(ins) #插入A股成交额和流通市值统计数据表
conn.close()
####################################@@@@@@获取深市A股数据结束@@@@@@@@@@@###############################################################

####################################执行SQL并获取相应的数据集DATAFRAME,并根据DATAFRAME绘折线图##########################################


####################################启动定时任务,以在每天16点发起以上所有操作，同时弹出历史趋势图#######################################