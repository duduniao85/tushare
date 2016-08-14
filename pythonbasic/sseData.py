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
driver.find_element_by_name("txtDate").clear()
#设置统计数据的数据日期
driver.find_element_by_name("txtDate").send_keys("2016-08-05")
#点击查询按钮
driver.find_element_by_id("1804_tab1_btn").click()
time.sleep(1)
   #股票总成交金额 ，从CHROME自带的“检查”功能获取XPATH路径为  //*[@id="REPORTID_tab1"]/tbody/tr[2]/td[3]
total_tradeamt=driver.find_element_by_xpath("//*[@id='REPORTID_tab1']/tbody/tr[2]/td[3]").text
    #股票总流通市值 //*[@id="REPORTID_tab1"]/tbody/tr[2]/td[8]
negotiableValue=driver.find_element_by_xpath('//*[@id="REPORTID_tab1"]/tbody/tr[2]/td[8]').text
    #b股总成交金额
tradeamtB=driver.find_element_by_xpath('//*[@id="REPORTID_tab1"]/tbody/tr[4]/td[3]').text
    #b股总流通市值
negotiableValueB=driver.find_element_by_xpath('//*[@id="REPORTID_tab1"]/tbody/tr[4]/td[8]').text
driver.quit()
# 深市A股总流通市值为深市总市值减去深市B股总市值
negotiableValueA_sz=int(negotiableValue.replace(',',''))-int(negotiableValueB.replace(',',''))
# 深市A股总成交额为深市总成交额减去深市B股总成交额
tradeamtA_sz=int(total_tradeamt.replace(',',''))-int(tradeamtB.replace(',',''))
#打印A股流通市值和成交金额
print negotiableValueA_sz,tradeamtA_sz

##################################取上交所相关统计数据###############################################
#开始按每个交易日循环
#remove readonly attribute
driver=webdriver.Chrome()
driver.get("http://www.sse.com.cn/market/stockdata/overview/day/")
#确保页面加载完毕，后续修改DOM元素只读属性成功
time.sleep(1)
#去掉元素的只读属性
driver.execute_script("var setDate=document.getElementById('start_date2');setDate.removeAttribute('readonly');")
#定位到日期控件
setDatElement=driver.find_element_by_xpath("//input[@id='start_date2']")
#清除内容
setDatElement.clear()
#重新填上指定的值
setDatElement.send_keys("2016-08-05")
#点击“查询”按钮
driver.find_element_by_id("btnQuery").click()
time.sleep(1)
negotiableValueA_sh=driver.find_element_by_xpath('//*[@id="tableData_934"]/div[2]/table/tbody/tr[3]/td[3]/div').text
#取最新的沪市A股成交金额 //*[@id="tableData_934"]/div[2]/table/tbody/tr[5]/td[3]/div
trdAmtA_sh=driver.find_element_by_xpath('//*[@id="tableData_934"]/div[2]/table/tbody/tr[5]/td[3]/div').text
#取最新的沪市A股平均市盈率
profitRateA_sh=driver.find_element_by_xpath('//*[@id="tableData_934"]/div[2]/table/tbody/tr[7]/td[3]/div').text
print negotiableValueA_sh,trdAmtA_sh,profitRateA_sh
driver.quit()
