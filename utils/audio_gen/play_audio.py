# -*- coding:utf-8 -*-
#
#   author: iflytek
#
#  本demo测试时运行的环境为：Windows + Python3.7
#  本demo测试成功运行时所安装的第三方库及其版本如下：
#   cffi==1.12.3
#   gevent==1.4.0
#   greenlet==0.4.15
#   pycparser==2.19
#   six==1.12.0
#   websocket==0.2.1
#   websocket-client==0.56.0
#   合成小语种需要传输小语种文本、使用小语种发音人vcn、tte=unicode以及修改文本编码方式
#  错误码链接：https://www.xfyun.cn/document/error-code （code返回错误码时必看）
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import os
import numpy as np
from pydub import AudioSegment
from utils.tools import get_project_path

demo_pcm_file = os.path.join(get_project_path(),'output','demo.pcm')


STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识


def on_message(ws, message):

    try:
        message = json.loads(message)
        code = message["code"]
        sid = message["sid"]
        audio = message["data"]["audio"]
        audio = base64.b64decode(audio)  # Convert the base64 audio data to bytes
        status = message["data"]["status"]
        
        if status == 2:
            # print("ws is closed")
            ws.close()
        if code != 0:
            errMsg = message["message"]
            print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))
        else:
            # print("pcm写入成功")
            with open(demo_pcm_file, 'ab') as f:
                f.write(audio)
      
            
    except Exception as e:
        print("receive msg, but parse exception:", e)


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws):
    print("### closed ###")


# 收到websocket连接建立的处理
def on_open(ws):
    def run(*args):
        APPID='ac0d049c'
        APISecret='MTIyMzY2ZGEwMjJlNDkyNzU3N2JhYjU3'
        APIKey='f3893454045f4e3dea21444b2b505df8'
        global content_user
        Text=content_user
        # 公共参数(common)
        CommonArgs = {"app_id": APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        BusinessArgs = {"aue": "raw", "auf": "audio/L16;rate=16000","vcn": "xiaoyan", "tte": "utf8"}# "sfl":1, 
        Data = {"status": 2, "text": str(base64.b64encode(Text.encode('utf-8')), "UTF8")}
        d = {"common": CommonArgs,
            "business": BusinessArgs,
            "data": Data,
        }
        d = json.dumps(d)
        # print("------>开始发送文本数据")
        ws.send(d)
        if os.path.exists(demo_pcm_file):
            os.remove(demo_pcm_file)

    thread.start_new_thread(run, ())

def create_url(APPID,APISecret,APIKey,CommonArgs,BusinessArgs,Data):
    url = 'wss://tts-api.xfyun.cn/v2/tts'
    # 生成RFC1123格式的时间戳
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))

    # 拼接字符串
    signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
    signature_origin += "date: " + date + "\n"
    signature_origin += "GET " + "/v2/tts " + "HTTP/1.1"
    # 进行hmac-sha256进行加密
    signature_sha = hmac.new(APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                digestmod=hashlib.sha256).digest()
    signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

    authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
        APIKey, "hmac-sha256", "host date request-line", signature_sha)
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
    # 将请求的鉴权参数组合为字典
    v = {
        "authorization": authorization,
        "date": date,
        "host": "ws-api.xfyun.cn"
        
    }
    # 拼接鉴权参数，生成url
    url = url + '?' + urlencode(v)
    # print("date: ",date)
    # print("v: ",v)
    # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
    # print('websocket url :', url)
    return url

def gen_audio(Text):
    # 测试时候在此处正确填写相关信息即可运行
    APPID='ac0d049c'
    APISecret='MTIyMzY2ZGEwMjJlNDkyNzU3N2JhYjU3'
    APIKey='f3893454045f4e3dea21444b2b505df8'
    # APPID='b280520e'
    # APISecret='ZGE4NmYxYTRkM2EyMzRiNGUyNWZiMzg4'
    # APIKey='2d7ea59e8fe2c6a462354e544a67fc0d'


    global content_user
    content_user=Text
    # 公共参数(common)
    CommonArgs = {"app_id": APPID}
    # 业务参数(business)，更多个性化参数可在官网查看
    BusinessArgs = {"aue": "raw", "auf": "audio/L16;rate=16000","vcn": "xiaoyan", "tte": "utf8"}# "sfl":1, 
    Data = {"status": 2, "text": str(base64.b64encode(Text.encode('utf-8')), "UTF8")}
    #使用小语种须使用以下方式，此处的unicode指的是 utf16小端的编码方式，即"UTF-16LE"”
    #self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-16')), "UTF8")}
    
    wsUrl = create_url(APPID,APISecret,APIKey,CommonArgs,BusinessArgs,Data)


    websocket.enableTrace(False)
    
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})



def text2audio(text,audio_file="output.wav"):
    """_summary_

    Args:
        text (_type_): _description_
        audio_file (str, optional): _description_. Defaults to "output.wav".

    Returns:
        _type_: 返回streamlit直接可以播放的wav byte文件
    """    
    # print(text)
    # print("**********************")
    gen_audio(text)
    
    # 读取PCM音频文件
    pcm_audio = AudioSegment.from_file(demo_pcm_file, format="raw", frame_rate=16000, channels=1, sample_width=2)

    # 将PCM音频转换为WAV格式
    wav_audio = pcm_audio.set_frame_rate(44100).set_channels(2)  # 设置适当的采样率和声道数
    wav_audio.export(audio_file, format="wav")

    # 读取转换后的WAV文件
    wav_bytes = open(audio_file, "rb").read()

    return wav_bytes