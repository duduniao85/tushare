#coding=utf-8
__author__ = 'xuyuming'
#########################创建和使用字典###############################
# ---------------------直接创建，ex.----------------------
phonebook={'Alice':'2341','Beth':'1234','Cecil':'3258'}
# 使用DICT函数创建,入参为序列或者其它字典
items=[('name','Gumby'),('age','42')]
d=dict(items)
# print d['name']
items=dict(name='Gumby',age='42')  #直接通过赋值语句创建字典
# print d['name']


#-----------------------字典的基本操作---------------------
print len(d)#长度
d['sex']='male'#增，改
del d['sex']#删除指定的项
# print d
print 'name' in d #查找，字典中查找键的效率更高

#---------------------- 字典的嵌套使用案例------------------
people = {
    'Alice':{
        'phone':'2341',
        'addr':'foo drive 1'
    },
     'Beth':{
        'phone':'1234',
        'addr':'foo drive 2'
    },
     'Cecil':{
        'phone':'3245',
        'addr':'foo drive 3'
    }
}
labels = {
    'phone':'phone number',
    'addr':'address'
}
#-----------以下为测试代码--------------------
# name = raw_input('Name: ')
# request = raw_input('Phone number(p) or address(a)?')#提示查找号码还是地址？
# if request == 'p':key = 'phone'
# if request == 'a':key = 'addr'
# if name in people : print "%s's%s is %s." % (name,labels[key],people[name][key])

#------------------------字典的格式化字符串--------------------------
print phonebook
template = '''<html>
<head><title>%(title)s</title></head>
<body>
<h1>%(title)s</h1>
<p>%(text)s</p>
</body>'''
data={'title':'My home page','text':'Welcome to my home page'}
print template%data  # 模板与实际数据发生了关联

#------------------------字典方法---------------------------------------
#clear 方法 ，会将原始字典的内容清空，






