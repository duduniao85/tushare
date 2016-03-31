#coding=utf-8
__author__ = 'xuyuming'
from urllib import urlopen
from BeautifulSoup import BeautifulSOAP
from bs4 import BeautifulSoup
text=urlopen('http://www.sipf.com.cn/subject/sub_ch/tjsj/index.html').read()
soup=BeautifulSoup(text)
print soup.originalEncoding
soup.prettify()
str='17,287'
print (int)(str.replace(',',''))
for tabb in  soup.findAll('table')[1:2]:
     tr_garanteebal=tabb.findAll('tr')[2]
     date=tr_garanteebal.findAll('p')[0].string #获取证券交易结算资金的日期时间段
     endvolume= tr_garanteebal.findAll('p')[2].string#获取证券交易结算资金的期末余额
     avgvolume=tr_garanteebal.findAll('p')[3].string#获取证券交易结算资金的平均余额
     involume=tr_garanteebal.findAll('p')[4].string#获取证券交易结算资金的转入额
     outvolume=tr_garanteebal.findAll('p')[5].string#获取证券交易结算资金的转出额
     print endvolume
# print date[0:4]+date[11:13]+date[-2:]+' '+(int)(endvolume.replace(',',''))+' '+(int)(avgvolume.replace(',',''))+' '+(int)(involume.replace(',',''))+' '+(int)(outvolume.replace(',',''))
#接下来将定义一个函数，用于执行指定的SQL语句以及连接指定的数据库



# 四大对象种类
# Tag
# NavigableString
# BeautifulSoup
# Comment


#以下是证券交易结算资金的变动情
 # <TR>
 #            <TD rowSpan=3 width=100 colSpan=2>
 #                <P align=center><font size=3>2016.03.21-03.25</font></P></TD>
 #            <TD vAlign=center width=130>
 #                <P align=center><font size=3>证券交易结算资金</font></P></TD>
 #            <TD vAlign=center width=90>
 #                <P align=center><font size=3>17,287</font></P></TD>
 #            <TD vAlign=center width=90>
 #                <P align=center><font size=3>17,718</font></P></TD>
 #            <TD vAlign=center width=100>
 #                <P align=center><font size=3>5,667</font></P></TD>
 #            <TD vAlign=center width=100>
 #                <P align=center><font size=3>5,608</font></P></TD>
 #            <TD vAlign=center width=120>
 #                <P align=center><font size=3>59</font></P></TD>
 #            <TD vAlign=center width=120>
 #                <P align=left><font size=3></font></P></TD>
 #        </TR>
