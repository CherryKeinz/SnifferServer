# -*-coding:utf-8-*-
import requests
import json
import os
import datetime
import time
from mongo_util import MyMongoDB
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def read_file(file_name):
	with open(file_name, 'r+') as f:
		pop_data = json.load(f)
	return pop_data

# data = read_file('json/_v1_game_resource_farm.json')
# print data


# 在crontab定时任务必须写绝对路径
rootdir = '/usr/keinz/project/WeloveAutoSign/json_y'
files = os.listdir(rootdir) #列出文件夹下所有的目录与文件
exe_seq = []
with open(os.path.join(rootdir, "exe_seq.txt"), 'r+') as f:
	exe_seq = [line.rstrip("\n") for line in f.readlines()]

# for i in range(0, len(files)):
for i, file_name in enumerate(exe_seq):
	path = os.path.join(rootdir,file_name)
	if os.path.isfile(path):
		time.sleep(1)
		content = read_file(path)
		headers = content['headers']
		url = "http://" + headers['Host'] + content['uri']
		data = content['data']
		print content['uri']
		d = requests.post(url,data=data,headers=headers)
		print d.text
		result = json.loads(d.text)
		# 存成文件的方式
		# with open('log/k' + files[i], 'w+') as f:
		# 	f.writelines(json.dumps(result) + '\n')

		# Record记录存到mongo
		if "records" in url:
			try:
				mongo = MyMongoDB('welove', 'records')
				if i == 0:
					mongo.delete({"user":"yun"})
				mongo.insert({"user":"yun","result":result})
			except Exception as e:
				raise e

		# # 所有结果存入mongo
		# try:
		# 	mongo = MyMongoDB('welove', 'result')
		# 	if i == 0:
		# 		mongo.delete({"user":"yun"})
		# 	mongo.insert({"user":"yun","result":result})
		# except Exception as e:
		# 	raise e

		# if result['result'] == 160:
		# 	with open('/usr/keinz/project/welove/log/sign_error_log.txt', 'a+') as f:
		# 		f.writelines(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
		# 		f.writelines(url + '\n')
		# 		f.writelines(json.dumps(content) + '\n')
		# 		f.writelines(json.dumps(result) + '\n')
