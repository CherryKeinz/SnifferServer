from flask import Flask, request, render_template
import sys
import time
import threading
from multiprocessing import Process
sys.path.append('../')
from module.task import Task



app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    if '39.106.54.239' == request.remote_addr:
        return render_template('index.html')
    return render_template('index.html')
    return render_template('404.html')

@app.route('/stop', methods=['GET'])
def stop():
    task = Task()
    task.stop_sniffer()
    return render_template('index.html')

@app.route('/start/<name>', methods=['GET'])
def start(name):
    #if '39.106.54.239' != request.remote_addr:
        #return render_template('404.html')
    if name == 'k' or name == 'y':
        task = Task()
        if task.is_task_running():
            return render_template('wait.html')
        task.start_sniffer(name)
        return render_template('running.html')
    else:
        return render_template('404.html')


# @app.route('/test', methods=['GET'])
# def test():
#     ip = request.remote_addr
#     url = request.url
#     print ip,
#     print url
#     return "this is test: "+str(ip)+str(url)



if __name__ == '__main__':
    # app.run(debug=True, threaded=False,port=8083,host='172.17.236.54')
    app.run(debug=True, threaded=False,port=8083,host='localhost')



