from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
import hashlib
import json
import xmltodict 
import  time

@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')
@app.route('/api/talk', methods=['POST'])
def talk():
    """
    :return: 返回index页面
    """
    print(''**************')
    print('**************',request.data)
   
    xml_to_dct = xmltodict.parse(request.data)
    print(xml_to_dct)
    xml_dict = xml_to_dct.get("xml")

    #提取信息
    msg_type = xml_dict.get("MsgType")
    resp_dict = {}
    if msg_type == "text":
        #表示发送的文本信息
        #构造返回值,经由微信服务器回复给用户的内容
        resp_dict = {
            "xml":{
                "ToUserName":xml_dict.get("FromUserName"),
                "FromUserName":xml_dict.get("ToUserName"),
                "CreateTime":int(time.time()),
                "MsgType":"text",
                "Content":xml_dict.get("Content")+'，王总'
            }
        }

    resp = xmltodict.unparse(resp_dict)
    return  resp

@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)
