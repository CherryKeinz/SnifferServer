#!/usr/bin/env python
# -*- coding:utf-8 -*-
import hashlib
from pymongo import MongoClient


settings = {
    "ip":'localhost',   #ip
    "port":27017,           #端口
}

class MyMongoDB(object):
    def __init__(self, db_name, set_name):
        try:
            self.conn = MongoClient(settings["ip"], settings["port"])
        except Exception as e:
            print(e)
        self.db = self.conn[db_name]
        # self.db.authenticate("keinz", "keinzkeinz", "SCRAM-SHA-256")
        self.my_set = self.db[set_name]

    def insert(self,dic):
        print("insert...")
        self.my_set.insert(dic)

    def update(self,newdic,dic={}):
        print("update...")
        self.my_set.update(dic, {"$set":newdic}, upsert=True)

    def delete(self,dic=None):
        print("delete...")
        self.my_set.remove(dic)

    def dbfind(self,dic=None):
        print("find...")
        return list(self.my_set.find(dic))


# mongo = MyMongoDB('welove', 'test')
# mongo.delete()
# mongo.update({"name":"kai","psw": "psw2"})
# print mongo.dbfind({"name":"kai"})
# m = hashlib.md5()
# m.update(b'yun')
# mongo.insert({"name":"kai","psw": m.hexdigest()})
# m.update(b'kai')
# mongo.insert({"name":"yun","psw": m.hexdigest()})
# print mongo.dbfind({"name":"kai"})
