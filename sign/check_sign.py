# -*- coding: utf-8 -*-
from mongo_util import *
from mail_util import *
from bson import json_util
import datetime
import os
import requests
import json
import time
from mongo_util import MyMongoDB


email_addr_dict = {
    "kai": "553636890@qq.com",
    "yun": ""
}
def read_file(file_name):
    with open(file_name, 'r+') as f:
        pop_data = json.load(f)
    return pop_data

class my_check(object):
    def __init__(self, user):
        self.user = user
    def get_status_by_post(self):
        rootdir = '/usr/keinz/project/WeloveAutoSign/json_k'
        files = os.listdir(rootdir) #列出文件夹下所有的目录与文件
        records_list = []
        for i in range(0, len(files)):
            if('records' in files[i]):
                path = os.path.join(rootdir,files[i])
                if os.path.isfile(path):
                    time.sleep(1)
                    content = read_file(path)
                    headers = content['headers']
                    url = "http://" + headers['Host'] + content['uri']
                    data = content['data']
                    d = requests.post(url,data=data,headers=headers)
                    result = json.loads(d.text)
                    if 'messages' in result:
                        records_list.append(result['messages'][0]['record'])
                        records_list.append(result['messages'][0]['lover_records'])
                    else:
                        records_list.append(result['records'])
                        records_list.append(result['lover_records'])
        return self.check_today(records_list)

    def check_today(self, records_list):
        today = datetime.datetime.today().date()
        result = 1
        for record in records_list:
            for item in record:
                day = item['date']
                day = datetime.datetime.strptime(day, '%Y-%m-%d').date()
                if day == today:
                    result &= item['complete']
                    print(item)
        return True if result == 1 else False

    def check_and_mail(self):
        sign_status = self.get_status_by_post()
        mail = my_mail("kai_keinz@163.com")
        if not sign_status:
            mail.send_mail("今天没有签到，赶紧手动签到，检查哪里出问题了！")


class my_check_by_mongo(object):
    def __init__(self, user):
        self.user = user 

    def get_status_by_post(self):
        try:
            mongo = MyMongoDB('welove', 'records')
            records = mongo.dbfind()
            records_list = []
            for record in records:
                result = record["result"]
                if 'messages' in result:
                    records_list.append(result['messages'][0]['record'])
                    records_list.append(result['messages'][0]['lover_records'])
                else:
                    records_list.append(result['records'])
                    records_list.append(result['lover_records'])
        except Exception as e:
            raise e
        return self.check_today(records_list)

    def check_today(self, records_list):
        today = datetime.datetime.today().date()
        result = 1
        for record in records_list:
            for item in record:
                day = item['date']
                day = datetime.datetime.strptime(day, '%Y-%m-%d').date()
                if day == today:
                    result &= int(item['complete'])
                    print(item)
        return True if result == 1 else False

    def check_and_mail(self):
        sign_status = self.get_status_by_post()
        mail = my_mail("kai_keinz@163.com")
        if not sign_status:
            mail.send_mail("今天没有签到，赶紧手动签到，检查哪里出问题了！")

class my_check_old(object):
    def __init__(self, user):
        self.user = user


    def get_sign_status(self):
        mongo = MyMongoDB('welove', 'result')
        result_list = mongo.dbfind({"user": self.user})
        # with open('check.json','w+') as f:
        #     f.writelines(json_util.dumps(result_list) + '\n')
        for result in result_list:
            for key in result['result'].keys():
                if 'go_home' in key:
                    return result['result']

    def is_not_sign(self, sign_status):
        mongo = MyMongoDB('welove', 'firstSignDate')
        result = mongo.dbfind({"user": self.user})[0]
        cur = datetime.datetime.now()
        first_date_tree = datetime.datetime.strptime(result["tree_date"],"%Y-%m-%d")
        delta_tree = (cur-first_date_tree).days
        first_date_home = datetime.datetime.strptime(result["home_date"],"%Y-%m-%d")
        delta_home = (cur-first_date_home).days
        print ("回家应签到%d天，已经签到%d天" % (delta_home, sign_status['go_home']))
        print ("树应签到%d天，已经签到%d天" % (delta_tree, sign_status['care_tree']))
        #print ("农场应签到%d天，已经签到%d天" % (delta_tree, sign_status['farm_time']))
        # if sign_status['go_home'] != delta_home or sign_status['farm_time'] != delta_tree or sign_status['care_tree'] != delta_tree:
        if sign_status['go_home'] != delta_home or sign_status['care_tree'] != delta_tree:
            return True
        else:
            return False



    def check_sign(self):
    	sign_status = self.get_sign_status()
    	mail = my_mail("kai_keinz@163.com")

        if sign_status == None:
            mail.send_mail(self.user + "签到系统出错了，赶紧检查一哈！")
        elif self.is_not_sign(sign_status):
            mail.send_mail(self.user + "今天没有签到，赶紧手动签到，检查哪里出问题了！")
        else:
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": "+ self.user + "签到成功！")

if __name__ == '__main__':
    check = my_check_by_mongo("kai")
    check.check_and_mail()
    # check = my_check("yun")
    # check.check_and_mail()
