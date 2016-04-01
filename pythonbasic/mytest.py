__author__ = 'xuyuming'
import tushare as ts
# ts.get_h_data(code='399106',index=True,end='2016-03-31')
# print ts.get_h_data(code='000001',start='2013-01-01',index=True,autype=None)
df=ts.get_today_all()
print df['nmc'].sum()#总流通市值
print df['volumn'].sum()#总成交金额
#将日期与交易日进行判断，如果日期为交易日，则启动将总流通市值和成交金额自动落地的程序,连同其它数据一起落地，利用APScheduler完成定时任务的启动

####################################获取一段时间内的日期是否为交易日，isOpen=1是交易日，isOpen=0为休市#####################
# mt = ts.Master()
# df = mt.TradeCal(exchangeCD='XSHG', beginDate='20150928', endDate='20151010', field='calendarDate,isOpen,prevTradeDate')
