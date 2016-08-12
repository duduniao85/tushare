#encoding:utf8
"""
@author:xuyuming
@contact:283548048@qq.com
@time:2016/8/8 22:47
""" 

from selenium import webdriver
import time

###############################取深交所相关统计数据#################################################
driver=webdriver.Chrome()
driver.get("http://www.szse.cn/main/marketdata/tjsj/jyjg/")
#抓取上交所交易日历数据
#开始按每个交易日循环
driver.find_element_by_name("txtDate").clear()
driver.find_element_by_name("txtDate").send_keys("2016-08-05")##2016-08-05 取相关统计数据的数据日期，每个交易日都取出来
driver.find_element_by_id("1804_tab1_btn").click()
time.sleep(1)
   #股票总成交金额 //*[@id="REPORTID_tab1"]/tbody/tr[2]/td[3]
total_tradeamt=driver.find_element_by_xpath("//*[@id='REPORTID_tab1']/tbody/tr[2]/td[3]").text
    #股票总流通市值 //*[@id="REPORTID_tab1"]/tbody/tr[2]/td[8]
negotiableValue=driver.find_element_by_xpath('//*[@id="REPORTID_tab1"]/tbody/tr[2]/td[8]').text
    #b股总成交金额
tradeamtB=driver.find_element_by_xpath('//*[@id="REPORTID_tab1"]/tbody/tr[4]/td[3]').text
    #b股总流通市值
negotiableValueB=driver.find_element_by_xpath('//*[@id="REPORTID_tab1"]/tbody/tr[4]/td[8]').text
driver.quit()
negotiableValueA_sz=int(negotiableValue.replace(',',''))-int(negotiableValueB.replace(',',''))   # 深市A股总流通市值为深市总市值减去深市B股总市值
tradeamtA_sz=int(total_tradeamt.replace(',',''))-int(tradeamtB.replace(',','')) # 深市A股总成交额为深市总成交额减去深市B股总成交额
print negotiableValueA_sz,tradeamtA_sz


##################################取上交所相关统计数据###############################################
#开始按每个交易日循环
#remove readonly attribute
driver.executeScript("var setDate=document.getElementById('start_date2');setDate.removeAttribute('readonly');")
#定位到日期控件
setDatElement=driver.findElement(By.xpath("//input[@id='train_date']"))
#清除内容
setDatElement.clear();
#重新填上指定的值
setDatElement.sendKeys("2015-02-18");
#点击“查询”按钮