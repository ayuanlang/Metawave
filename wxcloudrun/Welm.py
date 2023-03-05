import requests
#微信语言模型接口API
def WeLM(prompt = "元浪",
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
    # The quota is reset every 24 hours (starting from the first request, within the next 24 hours).

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
    
  
    if n != 1:# 若返回多条消息，则返回最多字数的那一条
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
    

print('t:'+WeLM(prompt='我是谁？'))