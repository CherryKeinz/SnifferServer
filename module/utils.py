# -*- coding: utf-8 -*-
import json
import time
from urllib import unquote
class Utils(object):

    def save_data(self, message_list, user_name):
        method =  message_list[0].split(' ')[0]
        uri_ =  message_list[0].split(' ')[1]
        params = {}
        headers = {}
        req_dict = {}
        if '?' in uri_:
            uri = uri_.split('?')[0]
            # params = dict([(param.split('=')[0], param.split('=')[1]) for param in uri_.split('?')[1].split('&')])
        else:
            uri = uri_

        for item in message_list[1:]:
            if ':' in item:
                headers[item.split(': ')[0]] = item.split(': ')[1]
            elif item != '':
                params = dict([(param.split('=')[0], param.split('=')[1]) for param in item.split('&')])
        if params.has_key('sig'):
            params['sig'] = unquote(params['sig'])

        req_dict['headers'] = headers
        req_dict['data'] = params
        req_dict['uri'] = uri_
        req_dict['method'] = method
        file_name = uri.replace('/', '_')
        if params.has_key('op'):
            file_name = file_name+ '_' + params['op']
        if params.has_key('task_type'):
            file_name = file_name+ '_' + params['task_type']
        # file_name = 'json_' + user_name + '/' + str(index)
        with open('json_' + user_name + '/' + "exe_seq.txt", 'a+') as f:
            f.writelines(file_name + '.json' +'\n')
        with open('json_' + user_name + '/' + file_name + '.json', 'w+') as f:
            json.dump(req_dict, f)
        print(file_name + " is already writen")
