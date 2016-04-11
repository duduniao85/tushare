#coding=utf-8
__author__ = 'xuyuming'
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'   #解决中文乱码问题
from urllib import urlopen
from bs4 import BeautifulSoup
from sqlalchemy import *
from sqlalchemy.dialects.oracle import \
            BFILE, BLOB, CHAR, CLOB, DATE, \
            DOUBLE_PRECISION, FLOAT, INTERVAL, LONG, NCLOB, \
            NUMBER, NVARCHAR, NVARCHAR2, RAW, TIMESTAMP, VARCHAR, \
            VARCHAR2
from sqlalchemy.sql import select
from sqlalchemy.sql import text #用于导入自定义文本SQL
from sqlalchemy.schema import *
import pandas as pd
import tushare as ts
import re
import matplotlib.pyplot as plt
#开始取上次数据日期



df=ts.get_hist_data('sh',start='2010-01-01')#开始取上证指数增量日期当中的行情数据
textdata=urlopen('http://www.sipf.com.cn/subject/sub_ch/tjsj/index.html').read()#取官方网站当中保证金余额变动数据
soup=BeautifulSoup(textdata)
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
textdata=urlopen('http://www.sse.com.cn/market/stockdata/overview/day/').read()#取官方网站当中保证金余额变动数据
print textdata
#取最新的沪市A股数据日期
m= re.search(r'searchDate\ \=\ \'([0-9]+\-[0-9]+\-[0-9]+)\'',textdata)
searchDate=m.group(1)
#取最新的沪市A股流通市值
m= re.search(r'negotiableValueA\ \=\ \'([0-9]+\.[0-9]+)\'',textdata)
negotiableValueA_sh=m.group(1)
#取最新的沪市A股成交金额
m= re.search(r'trdAmtA\ \=\ \'([0-9]+\.[0-9]+)\'',textdata)
trdAmtA_sh=m.group(1)
#取最新的沪市A股平均市盈率
m= re.search(r'profitRateA\ \=\ \'([0-9]+\.[0-9]+)\'',textdata)
profitRateA_sh=m.group(1)
print negotiableValueA_sh,trdAmtA_sh,profitRateA_sh,searchDate



####################################获取深市A股数据开始########################################
textdata=urlopen('http://www.szse.cn/main/marketdata/tjsj/jyjg/').read()
soup=BeautifulSoup(textdata)
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

db_engine=create_engine('oracle+cx_oracle://quant:1@127.0.0.1:1521/XE', echo=True)
meta=MetaData()
conn=db_engine.connect()
result=conn.execute(s).fetchall() #取得所有结果集合LIST
s=("select t1.tradeday "
",(t1.avgvolume * 200000000/t2.liutongshizhi-0.0524763282816744)/(0.1545725264839-0.0524763282816744) "
" as grtvol_liutongshizhi "
",(t2.chengjiajine / t1.avgvolume / 200000000-0.0874382438006733)/(0.453180473372781-0.0874382438006733) "
"as tradevol_grtvol     "
",(t3.close-1950.01)/(5166.35-1950.01) as closeprice_sh "
"  from guarantee_balance t1, a_gu_stat t2,shangzhengzongzhi t3 "
" where t1.tradeday = t2.tradeday  and t2.tradeday>'2013-01-01'"
"   and t2.tradeday = t3.\"date\" ")
selectsql = text(s)
result=conn.execute(selectsql) #执行查询语句
df_result=pd.DataFrame(result.fetchall())
df_result.columns=['TRADEDAY','GRTVOL_LIUTONGSHIZHI','TRADEVOL_GRTVOL','CLOSEPRICE_SH']
df_result=df_result.set_index('TRADEDAY')
print df_result.index
df_result['GRTVOL_LIUTONGSHIZHI'].astype(float).plot()
df_result['TRADEVOL_GRTVOL'].astype(float).plot()
df_result['CLOSEPRICE_SH'].astype(float).plot()
plt.legend() #显示图例
plt.grid(true)
plt.show() #展示绘图
conn.close() #展示
#####################################调用通联函数，取A股历史行情##################################################################################
db_engine=create_engine('oracle+cx_oracle://quant:1@127.0.0.1:1521/XE?charset=utf8', echo=True)
conn=db_engine.connect()
df=ts.get_stock_basics()
# df.to_sql('stock_basics',db_engine,if_exists='replace',dtype={'code': CHAR(6), 'name':VARCHAR2(128), 'area':VARCHAR2(128),\
#                                                               'industry':VARCHAR2(128)})
#开始归档前复权历史行情至数据库当中，以便可以方便地计算后续选股模型
for code in   df.index:
     df_h_data=ts.get_h_data(code,start='2015-12-31')
     df_h_data['secucode']=code
     df_h_data.to_sql('h_dailyquote',db_engine,if_exists='append',dtype={'secucode': CHAR(6)})
conn.close()
#####################################调用指定存储过程，获取最近一周成交量突然放大，但是股价涨幅在2%以内的股票#####################################
#####################################启动定时任务,以在每天16点发起以上所有操作，同时弹出历史趋势图################################################
#####################################获取市值200亿以内的股票清单，同时评估相关股票的市值数据 #####################################################


