__author__ = 'xuyuming'
import tushare as ts
# ts.get_h_data(code='399106',index=True,end='2016-03-31')
# print ts.get_h_data(code='000001',start='2013-01-01',index=True,autype=None)
df=ts.get_today_all()
print df['nmc'].sum()#����ͨ��ֵ
print df['volumn'].sum()#�ܳɽ����
#�������뽻���ս����жϣ��������Ϊ�����գ�������������ͨ��ֵ�ͳɽ�����Զ���صĳ���,��ͬ��������һ����أ�����APScheduler��ɶ�ʱ���������

####################################��ȡһ��ʱ���ڵ������Ƿ�Ϊ�����գ�isOpen=1�ǽ����գ�isOpen=0Ϊ����#####################
# mt = ts.Master()
# df = mt.TradeCal(exchangeCD='XSHG', beginDate='20150928', endDate='20151010', field='calendarDate,isOpen,prevTradeDate')
