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
import logging
from logging import FileHandler

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
    params = request.get_json()
    for key in params.items():
        app.logger.info(key)
    article_info = {}
    data = json.loads(json.dumps(article_info))
    app.logger.info('hhhhhhhhhhhhhhhhhhhhh')
    data['ToUserName'] = params['FromUserName']
    data['FromUserName'] = params['ToUserName']
    data['MsgType'] = 'text'
    data['CreateTime'] = int(time.time())
    if '我爱你' in params['Content']:
        data['Content'] = '我爱你'
    elif '猪' in params['Content']:
        data['Content'] = params['Content']      
    else:
        #data['Content'] = '王总，您是说：'+params['Content']+' 吗？元浪完全没法和你沟通/:8-)，还是去双溪玩吧'
        data['Content']=Welm(prompt=params['Content'])
    
    app.logger.info(json.dumps(data,ensure_ascii=False))
    app.logger.info('bbbbbbbbbbbbbbbb')
    return json.dumps(data,ensure_ascii=False)

    
    
    

    
   


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
def Welm(prompt = "元浪",
        Authorization = 'cfe7mpr2fperuifn6amg',
         model = 'xl',
         max_tokens = 64,
         temperature = 0.85,
         top_p = 0.95,
         top_k = 50,
         n = 5,
         echo=False,
         stop = ',，.。'):
    

    # Up to 30 requests every 1 minute for each token.
    # Up to 1000000 characters can be generated every 24 hours.
    # The quota is reset every 24 hours (starting from the first request,

    headers = {
        # 个人授权码
        'Authorization': Authorization,
    }
    
    json_data = {
        #提示词
        'prompt': prompt,
        'model': model,
        'max_tokens': max_tokens,
        'temperature': temperature,
        'top_p': top_p,
        'top_k': top_k,
        'n': n,
        'echo': echo,
        'stop': stop,
    }
    
      response = requests.post('https://welm.weixin.qq.com/v1/completions', headers=headers, json=json_data)
    
  
    if n > 1:
        stack = [[]]
        rcontent='let me think'
        try:            
            print('kkkkkkkkkkkkkkk')
            for i in eval(response.text)['choices']:
               
                if len(i['text'])>0:
                    rcontent = (i['text'].split('\n'))[0]
                
            print('-'+rcontent+len(rcontent))
            
            
        except:
            pass

        return rcontent
    
    else:# 返回第一条
        return eval(response.text)['choices'][0]['text']
