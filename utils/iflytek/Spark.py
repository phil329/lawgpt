
import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode, urlparse
from wsgiref.handlers import format_date_time

import websocket  # 使用websocket_client


class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, Spark_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(Spark_url).netloc
        self.path = urlparse(Spark_url).path
        self.Spark_url = Spark_url

    # 生成url
    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.Spark_url + '?' + urlencode(v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws,one,two):
    print(" ")


# 收到websocket连接建立的处理
def on_open(ws):
    thread.start_new_thread(run, (ws,))


def run(ws, *args):
    data = json.dumps(gen_params(appid=ws.appid, domain= ws.domain,question=ws.question))
    ws.send(data)


# 收到websocket消息的处理
def on_message(ws, message):
    # print(message)
    data = json.loads(message)
    code = data['header']['code']
    if code != 0:
        print(f'请求错误: {code}, {data}')
        ws.close()
    else:
        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]
        # print(content,end ="")
        global answer
        answer += content
        # print(1)
        if status == 2:
            ws.close()


def gen_params(appid, domain,question):
    """
    通过appid和用户的提问来生成请参数
    """
    data = {
        "header": {
            "app_id": appid,
            "uid": "1234"
        },
        "parameter": {
            "chat": {
                "domain": domain,
                "random_threshold": 0.5,
                "max_tokens": 2048,
                "auditing": "default"
            }
        },
        "payload": {
            "message": {
                "text": question
            }
        }
    }
    return data


class Spark(object):
    def __init__(self):
        self.appid = "f54bca1a"
        self.api_key = "2e7516edf376713eb5d99fc812a87ed5"
        self.api_secret = "ZGJmMjY3YWFmNGY5N2Q1YWMwOGZlMjFh"

        # 用于配置大模型版本，默认“generalv2”  云端环境的服务地址
        self.domain = "generalv2"
        self.Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址


    def _checklen(self,chat_list,length=8000):
        while (self._get_length(chat_list) > length):
            del chat_list[0]
        return chat_list
    
    def _get_all_content(self,chat_list):
        chat_list = self._checklen(chat_list,length=4000)
        res = ''
        for content in chat_list:
            res = content["content"]
        return res


    def _get_length(self,chat_list):
        length = 0
        for content in chat_list:
            temp = content["content"]
            leng = len(temp)
            length += leng
        return length

    def main(self,chat_list):
        global answer
        answer = ''

        chat_list = self._checklen(chat_list)
        wsParam = Ws_Param(self.appid, self.api_key, self.api_secret, self.Spark_url)
        websocket.enableTrace(False)
        wsUrl = wsParam.create_url()
        ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)
        ws.appid = self.appid
        ws.question = chat_list
        ws.domain = self.domain
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

        return answer

if __name__ == '__main__':
    api = Spark()

    prompt1 = [{'role':'asistant','content':'how can i help you?'},{'role':'user','content':'write me a bubble sort algorithm.'}]

    res = api.main(prompt1)
    print(res)

    prompt1.append({'role':'asistant','content':res})

    prompt2 = [{'role':'user','content':'what is the meaning of code above'}]
    
    res = api.main(prompt1+prompt2)
    print('--'*40)
    print(res)
    