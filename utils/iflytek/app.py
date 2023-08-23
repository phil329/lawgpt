from flask import Flask, request, jsonify, make_response
import hashlib
import hmac
import base64
import json
import time

import SparkApi

app = Flask(__name__)

appid = "e97d3136"
api_key = "b25338415789cf13a0091d64a1b3381e"
api_secret = "MDExMGZmZjFjMzRhOTkzNzczMGEyMzgw"

domain = "plugin"
Spark_url = "ws://spark-api-knowledge.xf-yun.com/v2.1/multimodal"

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text

@app.route('/')
def index():
   return 'Hello, World!'


@app.route('/chat', methods=['POST'])
def chat():
    text = request.json.get("text",[])
    if text.length == 0:
        response_data = {
        'code': -1,
        'text': []
        }
        response = make_response(jsonify(response_data))
        return response
    question = checklen(text)
    SparkApi.answer = ""
    SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
    jsoncon = {}
    jsoncon["role"] = "assistant"
    jsoncon["content"] = SparkApi.answer
    text.append(jsoncon)
     # 返回结果
    response_data = {
        'code': 20000,
        'text': text
    }
    response = make_response(jsonify(response_data))
    return response

if __name__ == '__main__':
    app.run(host='172.30.12.252', port=5001,debug=True)
