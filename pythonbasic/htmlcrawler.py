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
df=ts.get_hist_data('sh',start='2010-01-01')
text=urlopen('http://www.sipf.com.cn/subject/sub_ch/tjsj/index.html').read()
soup=BeautifulSoup(text)
print soup.originalEncoding
soup.prettify()
for tabb in  soup.findAll('table')[1:2]:
     tr_garanteebal=tabb.findAll('tr')[2]
     date=tr_garanteebal.findAll('p')[0].string #获取证券交易结算资金的日期时间段
     endvolume= tr_garanteebal.findAll('p')[2].string#获取证券交易结算资金的期末余额
     avgvolume=tr_garanteebal.findAll('p')[3].string#获取证券交易结算资金的平均余额
     involume=tr_garanteebal.findAll('p')[4].string#获取证券交易结算资金的转入额
     outvolume=tr_garanteebal.findAll('p')[5].string#获取证券交易结算资金的转出额
     tradeday=date[0:4]+date[11:13]+date[-2:]
     print endvolume
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
df.to_sql('his_daylyquote',db_engine,if_exists='append',dtype={'date': CHAR(10)})

#执行自定义SQL实现相关的数据
print ts.get_h_data(code='000001',index=True,start='',autype=None,end='2016-03-31')




# 四大对象种类
# Tag
# NavigableString
# BeautifulSoup
# Comment

