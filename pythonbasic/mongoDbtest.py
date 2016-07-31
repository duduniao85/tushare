#coding=utf-8
__author__ = 'Administrator'
import pymongo
client = pymongo.MongoClient('localhost',27017)
walden=client['walden']
sheet_lines=walden['sheet_lines']
path=r'd:\mongoTest.txt'
with open(path,'r') as f:
    lines=f.readlines()
    for index,line in enumerate(lines):
        data = {
            'index':index,
            'line':line,
            'words':len(line.split())
        }
        sheet_lines.insert_one(data)