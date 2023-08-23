import os
import sys
import json

from utils.iflytek.Spark import Spark
import streamlit as st
from streamlit_chat import message

from bokeh.models.widgets import Button
from bokeh.models import CustomJS

from streamlit_bokeh_events import streamlit_bokeh_events

from gtts import gTTS
from io import BytesIO
from utils.audio_gen.play_audio import text2audio

from utils.prompt_config_l import *
from utils.tools import transverse_on_json,extract_json_from_string,json2file,get_project_path,json2md
from utils.prompt_config import summary_chat_prompt
from utils.audio_gen.input_audio import js_code

import pytz
from datetime import datetime

systime=pytz.timezone('Asia/shanghai')
cur_time=datetime.utcnow()
cur_beijing=cur_time.replace(tzinfo=pytz.utc).astimezone(systime)
formattime=cur_beijing.strftime('%Y %m %d')

project_path = get_project_path()

api = Spark()

# ⛋ ✍
# st.title("✍ Legal Document Chatbot")


if 'is_audio' not in st.session_state:
    st.session_state['is_audio'] = True

if 'message_keys' not in st.session_state:
    st.session_state['message_keys'] = 0


if 'current_chat' not in st.session_state:
    st.session_state['current_chat'] = [{"role": "assistant", "content": start_chat}]
    st.session_state['message_keys'] = 0

if 'gen_keyget' not in st.session_state:
    st.session_state['gen_keyget'] =[]

if 'gen_keymiss' not in st.session_state:
    st.session_state['gen_keymiss'] =[]

if 'yuangao_data' not in st.session_state:
    st.session_state['yuangao_data'] ={'姓名': None, '性别': None, '出生日期': None, '民族': None, '住址': None, '联系方式': None, '身份证号': None, '法定代理人':None, '委托诉讼代理人': {'姓名': None, '事务所': None}}

if 'beigao_data' not in st.session_state:
    st.session_state['beigao_data'] ={'姓名': None, '性别': None, '出生日期': None, '民族': None, '住址': None, '联系方式': None, '身份证号': None, '法定代理人':None, '委托诉讼代理人': {'姓名': None, '事务所': None}}

if 'yuangao_company_data' not in st.session_state:
    st.session_state['yuangao_company_data'] ={ "公司名称": None, "公司所在地":  None, '统一社会信用代码': None, "法人": { "姓名": None, "职务": None, "联系方式": None},"委托诉讼代理人": {"姓名": None,"事务所": None}}

if 'beigao_company_data' not in st.session_state:
    st.session_state['beigao_company_data'] ={ "公司名称": None, "公司所在地":  None, '统一社会信用代码': None, "法人": { "姓名": None, "职务": None, "联系方式": None},"委托诉讼代理人": {"姓名": None,"事务所": None}}

if 'second_state' not in st.session_state:
    st.session_state['second_state'] = False

if 'third_state' not in st.session_state:
    st.session_state['third_state'] = False

if 'third_state_data' not in st.session_state:
    st.session_state['third_state_data'] = {"案由": None, "诉讼请求": None, "事实理由": None, "证据": None, "法院":None, "日期": formattime}

if 'third_state_step' not in st.session_state:
    st.session_state['third_state_step'] = 1

if 'fourth_state' not in st.session_state:
    st.session_state['fourth_state'] = False

if 'yuangao_list' not in st.session_state:
    st.session_state['yuangao_list'] = []

if 'beigao_list' not in st.session_state:
    st.session_state['beigao_list'] = []

if "is_person"not in st.session_state:
    st.session_state['is_person'] = False

if "is_company"not in st.session_state:
    st.session_state['is_company'] = False

if 'agent_flag_1' not in st.session_state:
    st.session_state['agent_flag_1'] = False

if 'agent_flag_2' not in st.session_state:
    st.session_state['agent_flag_2'] = False


if 'prompt2usr' not in st.session_state:
    st.session_state['prompt2usr'] = ""

if "cause_of_action" not in st.session_state:
    st.session_state['cause_of_action'] = ['机动车交通事故责任纠纷', '民间借贷纠纷', '离婚纠纷']

if "input_count" not in st.session_state:
    st.session_state['input_count'] = 0

if "last_gen_keymiss" not in st.session_state:
    st.session_state['last_gen_keymiss'] = 0

def clear_chat_history():
    temp = st.session_state['current_chat']

    if 'history_chat' not in st.session_state:
        st.session_state['history_chat'] = {}

    st.session_state['second_state'] = False
    st.session_state['third_state'] = False
    st.session_state['fourth_state'] = False
    st.session_state['third_state_step'] = 1
    st.session_state['yuangao_data'] ={'姓名': None, '性别': None, '出生日期': None, '民族': None, '住址': None, '联系方式': None, '身份证号': None, "法定代理人": None, '委托诉讼代理人': {'姓名': None, '事务所': None}}
    st.session_state['beigao_data'] ={'姓名': None, '性别': None, '出生日期': None, '民族': None, '住址': None, '联系方式': None, '身份证号': None, "法定代理人": None, '委托诉讼代理人': {'姓名': None, '事务所': None}}
    st.session_state['yuangao_company_data'] ={ "公司名称": None, "公司所在地":  None, '统一社会信用代码': None, "法人": { "姓名": None, "职务": None, "联系方式": None},"委托诉讼代理人": {"姓名": None,"事务所": None}}
    st.session_state['beigao_company_data'] ={ "公司名称": None, "公司所在地":  None, '统一社会信用代码': None, "法人": { "姓名": None, "职务": None, "联系方式": None},"委托诉讼代理人": {"姓名": None,"事务所": None}}
    st.session_state['third_state_data'] = {"案由": None, "诉讼请求": None, "事实理由": None, "证据": None, "法院":None, "日期": formattime}
    st.session_state['yuangao_list'] = []
    st.session_state['beigao_list'] = []
    st.session_state['is_person'] = False
    st.session_state['is_company'] = False
    st.session_state['agent_flag_1'] = False
    st.session_state['agent_flag_2'] = False
    st.session_state['prompt2usr'] = ""
    st.session_state['gen_keyget'] =[]

    temp = st.session_state['current_chat']
    content = api._get_all_content(st.session_state['current_chat'])
    abstract = api.main([{'role':'user','content':summary_chat_prompt+content}])

    index = len(st.session_state['history_chat'])

    title = str(index)+'.'+abstract
    st.session_state['history_chat'][title] = temp
    st.session_state['current_chat'] = [{"role": "assistant", "content": start_chat}]
    
    if 'category' in st.session_state:
        del st.session_state['category']
    
    if 'message_keys' in st.session_state:
        st.session_state['message_keys'] = 0
    

st.sidebar.subheader("全局设置")

st.sidebar.button('开启新对话', on_click=clear_chat_history,use_container_width=True)
# is_anonymous = st.sidebar.selectbox('匿名设置，是否允许我们收集您的信息',('yes','no'))
# is_anonymous = st.sidebar.radio("匿名设置，是否允许我们收集您的信息", ('yes', 'no'))
# st.session_state["is_anonymous"] = is_anonymous

# is_audio = st.sidebar.selectbox('是否语音输出',('no','yes'))
is_audio = st.sidebar.radio('是否语音输出',('Yes','No'))
st.session_state["is_audio"] = (is_audio == 'Yes')



# if 'category' not in st.session_state:
options = ('我不太清楚诶','机动车交通事故责任纠纷', '民间借贷纠纷', '离婚纠纷')
option = st.sidebar.selectbox(
    '🙋如果确定，请选择要生成诉讼文书的案由',
    options)
st.session_state['category'] = option
st.sidebar.write('🖊️ 当前任务：'+st.session_state['category'])

def judge_p_c(res_judge):
    for x in res_judge:
        if x in st.session_state.prompt:
            return True
    return False

    
def check_miss(data):
    keyget = []
    if st.session_state['agent_flag_1']:
        if "委托诉讼代理人" in data and "姓名" in data["委托诉讼代理人"]:
            if data["委托诉讼代理人"]["姓名"] is None:
                data["委托诉讼代理人"] = "无"
        st.session_state['agent_flag_1'] = False

    if st.session_state['agent_flag_2']:
        if "法定代理人" in data:
            if data["法定代理人"] is None:
                data["法定代理人"] = "无"
        st.session_state['agent_flag_2'] = False

    if isinstance(data,dict):
        keyget,keymiss=transverse_on_json(data)

    for x in keyget:
        if x == "住址" or x == "公司所在地":
            new_prompt_json={'role': 'user', 'content': data[x]+address_complete_json}
            res_json = api.main([new_prompt_json])
            data[x]=extract_json_from_string(res_json)["住址"]
        if st.session_state['is_person']==True:
            if st.session_state['second_state']:
                st.session_state['beigao_data'][x]=data[x]
            else:
                st.session_state['yuangao_data'][x]=data[x]
        if st.session_state['is_company']==True:
            if st.session_state['second_state']:
                st.session_state['beigao_company_data'][x]=data[x]
            else:
                st.session_state['yuangao_company_data'][x]=data[x]
        st.session_state['gen_keyget']+=keyget

    new_miss=[]

    for x in st.session_state['gen_keymiss']:
        if x not in st.session_state['gen_keyget']:
            new_miss.append(x)
    st.session_state['gen_keymiss']=new_miss

def excute_fourth():
    new_prompt_json={'role': 'user', 'content': st.session_state.prompt}
    res_answer=api.main([new_prompt_json])
    return res_answer

def excute_third():
    # 输入诉讼请求
    if st.session_state['third_state_step'] == 1:  
        res_answer="好的，我已经知道您的诉讼请求了，根据您的案由与诉讼请求，我为您生成了一份事实与理由模板：\n\n"
        if st.session_state['category'] == "民间借贷纠纷":
            res_answer += debt_usr_reason_prompt + "\n\n **请参考以上模板输入您的事实和理由。**"
            prompt = debt_usr_request_prompt
        if st.session_state['category'] == "机动车交通事故责任纠纷":
            res_answer += traffic_usr_reason_prompt + "\n\n **请参考以上模板输入您的事实和理由。**"
            prompt = traffic_usr_request_prompt
        if st.session_state['category'] == "离婚纠纷":
            res_answer += divorce_usr_reason_prompt + "\n\n **请参考以上模板输入您的事实和理由。**"
            prompt = divorce_usr_request_prompt
        new_prompt_json={'role': 'user', 'content': prompt+guide_second_step1+st.session_state.prompt}
        st.session_state['third_state_data']["诉讼请求"]=api.main([new_prompt_json])
        st.session_state['third_state_step'] = 2

    
    # 输入事实和理由
    elif st.session_state['third_state_step'] == 2:   
        if st.session_state['category'] == "民间借贷纠纷":
            prompt = debt_usr_reason_prompt
        if st.session_state['category'] == "机动车交通事故责任纠纷":
            prompt = traffic_usr_reason_prompt
        if st.session_state['category'] == "离婚纠纷":
            prompt = divorce_usr_reason_prompt
        new_prompt_json={'role': 'user', 'content': prompt+guide_second_step2+st.session_state.prompt}
        st.session_state['third_state_data']["事实理由"]=api.main([new_prompt_json])
        st.session_state['third_state_step']=3
        res_answer="好的，我已经知道你的诉讼请求了。请进一步告诉我您诉讼的**相关证据**。"

    elif st.session_state['third_state_step'] == 3:   
        new_prompt_json={'role': 'user', 'content': gudie_second_step3+st.session_state.prompt}
        st.session_state['third_state_data']["证据"]=api.main([new_prompt_json])
        st.session_state['third_state_step']=4
        res_answer="好的，我已经知道你的相关证据了。"
    
        # 根据被告信息推荐法院
        company_addresses = []
        for info in st.session_state['beigao_list']:
            if "住址" in info:
                company_address = info["住址"]
                company_addresses.append(company_address)
            if "公司所在地" in info:
                company_address = info["公司所在地"]
                company_addresses.append(company_address)
        all_addresses = ", ".join(company_addresses)
        
        new_prompt_json={'role': 'user', 'content': gudie_second_step4+all_addresses}
        recommend=api.main([new_prompt_json])
        
        res_answer = "如下是为您推荐的法院：" + recommend + "。请选择法院。"
        st.session_state['third_state_step'] = 5
    
    elif st.session_state['third_state_step'] == 5:   
        # 填写法院名称
        new_prompt_json={'role': 'user', 'content': gudie_second_step5+st.session_state.prompt}
        st.session_state['third_state_data']["法院"]=api.main([new_prompt_json])
        st.session_state['third_state_step']=5
        st.session_state['fourth_state']=True
        # st.session_state['yuangao_list'].append(st.session_state['yuangao_data'])
        # st.session_state['beigao_list'].append(st.session_state['beigao_data'])
        res_answer="好的，已为你生成了诉讼书。案由、诉讼请求、事实和理由的相关信息如下"+json.dumps(st.session_state['third_state_data'],ensure_ascii=False)
        res_answer="好的，已为你生成了诉讼书,您可以前往预览界面进行预览,如果您想继续生成一份诉状书，可以点击左边开启新对话。或者你可以和我继续聊天，我很乐意和你讨论法律相关知识。"
    else:
        res_answer="好的，已为你生成了诉讼书。案由、诉讼请求、事实和理由的相关信息如下"+json.dumps(st.session_state['third_state_data'],ensure_ascii=False)
    return res_answer

def excute_second():
    if st.session_state['is_person']==False and st.session_state['is_company']==False:
        #大模型判断是个人还是公司
        if "个人" in st.session_state.prompt and "公司" in st.session_state.prompt:
            res_1_2=3
        elif judge_p_c(res_judge_jj_3):
            res_1_2=3
        elif judge_p_c(res_judge_c_2):
            res_1_2=2
        elif judge_p_c(res_judge_p_1):
            res_1_2=1
        else:
            res_1_2=3
        # prompt_1_2={'role': 'user', 'content': gudie_1_2+prompt}
        # res_1_2 = api.main([prompt_1_2])
        
        if res_1_2==1:
            st.session_state['is_person']=True
            res_answer="谢谢您提供的信息！\n\n请告诉我 **自然人（个人）** 的如下信息\n* 姓名\n* 身份证号\n* 性别\n* 出生日期\n* 民族\n* 住址\n* 联系方式\n * 委托代理人（如有）\n * 法定代理人（如有）"
            st.session_state['gen_keymiss'] =["姓名", "性别", "出生日期", "民族", "住址","联系方式","委托诉讼代理人","身份证号","法定代理人"]
            st.session_state['last_gen_keymiss']=st.session_state['gen_keymiss']
            st.session_state['gen_keyget'] =[]
        elif res_1_2==2:
            st.session_state['is_company']=True
            res_answer="谢谢您提供的信息！\n\n请先告诉我 **非自然人（公司）** 的如下信息：\n* 公司名称\n* 统一社会信用代码\n *公司所在地\n* 法人的姓名、职务、联系方式"
            st.session_state['gen_keymiss'] =["公司名称", "公司所在地","法人","委托诉讼代理人","统一社会信用代码"]
            st.session_state['last_gen_keymiss']=st.session_state['gen_keymiss']
            st.session_state['gen_keyget'] =[]
        else:
            st.session_state['is_person']=False
            st.session_state['is_company']=False
            res_answer="不好意思，我不太清楚您的意思，请问被告的是个人还是公司呢"     
    
    elif st.session_state['is_person']==True and st.session_state['is_company']==False:
              
        new_prompt_json={'role': 'user', 'content': gudie_beigao_person_json+st.session_state["prompt2usr"]+st.session_state.prompt}
        res_json = api.main([new_prompt_json])
        data=extract_json_from_string(res_json)
        check_miss(data)
        if st.session_state['last_gen_keymiss']==st.session_state['gen_keymiss']:
            st.session_state['input_count']+=1
        else:
            st.session_state['input_count']=0
        if st.session_state['input_count']==3:
            st.session_state['input_count']=0
            for x in st.session_state['gen_keymiss']:
                st.session_state['beigao_data'][x]="无"
            st.session_state['beigao_list'].append(st.session_state['beigao_data'])
            st.session_state['is_person']=True
            st.session_state['is_company']=True
            res_answer="亲，发现您多次没有提供有效的"+','.jion(st.session_state['gen_keymiss'])+"信息，先帮你跳过吧！我已经知道第"+str(len(st.session_state['beigao_list']))+"个被告的信息了\n 请问你是否继续添加**被告**信息呢"
            return res_answer
        
        if len(st.session_state['gen_keymiss'])!=0:
            # res_answer="现在还不知道您的被告人的"+'，'.join(st.session_state['gen_keymiss'])+"信息，您能告诉我吗？"
            if "委托诉讼代理人" in st.session_state['gen_keymiss']:
                st.session_state['agent_flag_1'] = True
                res_answer="请问自然人是否有**委托代理人**？"
            elif "法定代理人" in st.session_state['gen_keymiss']:
                st.session_state['agent_flag_2'] = True
                res_answer="请问自然人是否有**法定代理人**？"
            else:
                res_answer="现在还不知道您的"+'，'.join(st.session_state['gen_keymiss'])+"信息，您能告诉我吗？"
        
        else:
            st.session_state['beigao_list'].append(st.session_state['beigao_data'])
            duo_yuangao="好的，我已经知道第"+str(len(st.session_state['beigao_list']))+"个被告的信息了，请问你是否需要继续添加被告信息"
            res_answer= duo_yuangao+"现在的被告的json文件如下"+json.dumps(st.session_state['beigao_list'],ensure_ascii=False)
            st.session_state['is_person']=True
            st.session_state['is_company']=True
    
    elif st.session_state['is_person']==False and st.session_state['is_company']==True:
        new_prompt_json={'role': 'user', 'content': gudie_beigao_company_json+st.session_state["prompt2usr"]+st.session_state.prompt}
        res_json = api.main([new_prompt_json])
        data=extract_json_from_string(res_json)
        check_miss(data)
        if st.session_state['last_gen_keymiss']==st.session_state['gen_keymiss']:
            st.session_state['input_count']+=1
        else:
            st.session_state['input_count']=0
        if st.session_state['input_count']==3:
            st.session_state['input_count']=0
            for x in st.session_state['gen_keymiss']:
                st.session_state['beigao_company_data'][x]="无"
            st.session_state['beigao_list'].append(st.session_state['beigao_company_data'])
            st.session_state['is_person']=True
            st.session_state['is_company']=True
            res_answer="亲，发现您多次没有提供有效的"+','.jion(st.session_state['gen_keymiss'])+"信息，先帮你跳过吧！我已经知道第"+str(len(st.session_state['beigao_list']))+"个被告的信息了\n 请问你是否继续添加**被告**信息呢"
            return res_answer
        if len(st.session_state['gen_keymiss'])!=0:
            if "委托诉讼代理人" in st.session_state['gen_keymiss']:
                st.session_state['agent_flag_1'] = True
                res_answer="请问被告公司是否有委托代理人？"
            else:
                res_answer="现在还不知道被告公司的"+'，'.join(st.session_state['gen_keymiss'])+"信息，您能告诉我吗？"
        else:
            st.session_state['beigao_list'].append(st.session_state['beigao_company_data'])
            duo_yuangao="好的，我已经知道第"+str(len(st.session_state['beigao_list']))+"个被告的信息了，请问你是否需要继续添加被告信息"
            res_answer= duo_yuangao+"现在的被告的json文件如下"+json.dumps(st.session_state['beigao_list'],ensure_ascii=False)
            st.session_state['is_person']=True
            st.session_state['is_company']=True
    elif st.session_state['is_person']==True and st.session_state['is_company']==True:
        if judge_p_c(res_judge_jj_3) and st.session_state['third_state_data']["案由"]==None:
            return "不好意思，没有听懂您的意思，请问你是否继续添加**被告**信息呢"
        elif (res_judge_no_2) or st.session_state['third_state_data']["案由"]=="不清楚":
            res_json=2
        elif judge_p_c(res_judge_go_1):
            res_json=1
        else:
            return "不好意思，没有听懂您的意思，请问你是否继续添加**被告**信息呢"
        if res_json==1:
            res_answer="好的,我会继续添加**被告**信息,请问你还想添加**个人**还是**公司**呢？"
            st.session_state['is_person']=False
            st.session_state['is_company']=False
        else:
            # 判断案由
            if st.session_state['category']=="我不太清楚诶" and st.session_state['third_state_data']["案由"]==None:
                res_answer="好的,我已经收集好了你的被告信息了。这边检测到您还没有选择**案由**，您可以在左边选择案由，若不清楚案件类型请简单描述一下案件情况，我会帮你**智能识别**案由"
                st.session_state['third_state_data']["案由"]="不清楚"
            elif st.session_state['category']=="我不太清楚诶" and st.session_state['third_state_data']["案由"]=="不清楚":
                new_prompt_json={'role': 'user', 'content': gudie_second_step0+st.session_state.prompt}
                anyou_str=api.main([new_prompt_json])
                # print(anyou_str)
                anyou=extract_json_from_string(anyou_str)["案由"]
                st.session_state['third_state_data']["案由"]=anyou
                res_answer="好的，已帮您识别案由为"+anyou
                if st.session_state['third_state_data']["案由"] in st.session_state['cause_of_action']:
                    if st.session_state['third_state_data']["案由"] == "民间借贷纠纷":
                        res_answer += "**,提示如下：\n\n" + debt_usr_request_prompt + "\n\n **请根据上述提示输入您的上诉请求。**"
                    if st.session_state['third_state_data']["案由"] == "机动车交通事故责任纠纷":
                        res_answer += "**,提示如下：\n\n" + traffic_usr_request_prompt + "\n\n **请根据上述提示输入您的上诉请求。**"
                    if st.session_state['third_state_data']["案由"] == "离婚纠纷":
                        res_answer += "**,提示如下：\n\n" + divorce_usr_request_prompt + "\n\n **请根据上述提示输入您的上诉请求。**"
                else:
                    res_answer="好的，已帮您识别案由为"+anyou+",请继续输入您的诉讼请求。"
                # st.session_state['third_state_step'] = 1
                # res_answer="好的，已帮您识别案由为"+anyou+",能进一步给出您的**事实和理由**吗？"
                st.session_state['third_state']=True
                st.session_state['second_state']=False
                st.session_state['gen_keymiss']=["案由", "诉讼请求", "事实理由", "证据", "法院", "日期"]
                st.session_state['gen_keyget'] =[]
            elif st.session_state['category']!="我不太清楚诶":#and st.session_state['third_state_data']["案由"]!="不清楚"
                st.session_state['third_state_data']["案由"]=st.session_state['category']
                st.session_state['third_state']=True
                st.session_state['second_state']=False
                st.session_state['gen_keymiss']=["案由", "诉讼请求", "事实理由", "证据", "法院", "日期"]
                st.session_state['gen_keyget'] =[]
                # res_answer="能进一步给出您的**事实和理由**吗？"
                st.sidebar.write('🖊️ 当前任务：'+st.session_state['category'])
                res_answer = "目前您的案由是**" + st.session_state['category']
                # 获取案由的提示信息
                if st.session_state['third_state_data']["案由"] in st.session_state['cause_of_action']:
                    if st.session_state['category'] == "民间借贷纠纷":
                        res_answer += "**,提示如下：\n\n" + debt_usr_request_prompt + "\n\n **请根据上述提示输入您的上诉请求。**"
                    if st.session_state['category'] == "机动车交通事故责任纠纷":
                        res_answer += "**,提示如下：\n\n" + traffic_usr_request_prompt + "\n\n **请根据上述提示输入您的上诉请求。**"
                    if st.session_state['category'] == "离婚纠纷":
                        res_answer += "**,提示如下：\n\n" + divorce_usr_request_prompt + "\n\n **请根据上述提示输入您的上诉请求。**"
                else:
                    res_answer+=",请继续输入您的诉讼请求。"


    return res_answer

def excute_first():
    if st.session_state['is_person']==False and st.session_state['is_company']==False:
        #大模型判断是个人还是公司
        if "个人" in st.session_state.prompt and "公司" in st.session_state.prompt:
            res_1_2=3
        elif judge_p_c(res_judge_jj_3):
            res_1_2=3
        elif judge_p_c(res_judge_c_2):
            res_1_2=2
        elif judge_p_c(res_judge_p_1):
            res_1_2=1
        else:
            res_1_2=3
        if res_1_2==1:
            st.session_state['is_person']=True
            res_answer="谢谢您提供的信息！\n\n请告诉我 **自然人（个人）** 的如下信息\n* 姓名\n* 身份证号\n* 性别\n* 出生日期\n* 民族\n* 住址\n* 联系方式\n * 委托代理人（如有）\n * 法定代理人（如有）"
            st.session_state['gen_keymiss'] =["姓名", "性别", "出生日期", "民族", "住址","联系方式","委托诉讼代理人","身份证号", "法定代理人" ]
            st.session_state['last_gen_keymiss']=st.session_state['gen_keymiss']
            st.session_state['gen_keyget'] =[]
        elif res_1_2==2:
            st.session_state['is_company']=True
            res_answer="谢谢您提供的信息！\n\n请先告诉我 **非自然人（公司）** 的如下信息：\n* 公司名称\n* 统一社会信用代码\n * 公司所在地\n* 法人的姓名、职务、联系方式"
            st.session_state['gen_keymiss'] =["公司名称", "公司所在地","法人","委托诉讼代理人", "统一社会信用代码"]
            st.session_state['last_gen_keymiss']=st.session_state['gen_keymiss']
            st.session_state['gen_keyget'] =[]
        else:
            st.session_state['is_person']=False 
            st.session_state['is_company']=False
            res_answer="不好意思，我不太清楚您的意思，请再告诉一次我**原告**的信息。\n\n请问原告是 *自然人（个人）* 还是 *非自然人（公司）* 呢？"     
    elif st.session_state['is_person']==True and st.session_state['is_company']==False:
        new_prompt_json={'role': 'user', 'content': gudie_yuangao_person_json+st.session_state['prompt2usr']+st.session_state.prompt}
        res_json = api.main([new_prompt_json])
        data=extract_json_from_string(res_json)
        check_miss(data)
        if st.session_state['last_gen_keymiss']==st.session_state['gen_keymiss']:
            st.session_state['input_count']+=1
        else:
            st.session_state['input_count']=0
        if st.session_state['input_count']==3:
            st.session_state['input_count']=0
            for x in st.session_state['gen_keymiss']:
                st.session_state['yuangao_data'][x]="无"
            st.session_state['yuangao_list'].append(st.session_state['yuangao_data'])
            st.session_state['is_person']=True
            st.session_state['is_company']=True
            res_answer="亲，发现您多次没有提供有效的"+','.jion(st.session_state['gen_keymiss'])+"信息，先帮你跳过吧！我已经知道第"+str(len(st.session_state['yuangao_list']))+"个被告的信息了\n 请问你是否继续添加**原告**信息呢"
            return res_answer
        if len(st.session_state['gen_keymiss'])!=0:
            if "委托诉讼代理人" in st.session_state['gen_keymiss']:
                st.session_state['agent_flag_1'] = True
                res_answer="请问自然人是否有**委托代理人**？"
            elif "法定代理人" in st.session_state['gen_keymiss']:
                st.session_state['agent_flag_2'] = True
                res_answer="请问自然人是否有**法定代理人**？"
            else:
                res_answer="现在还不知道您的"+'，'.join(st.session_state['gen_keymiss'])+"信息，您能告诉我吗？"
        
        else:
            st.session_state['yuangao_list'].append(st.session_state['yuangao_data'])
            duo_yuangao="好的，我已经知道**第"+str(len(st.session_state['yuangao_list']))+"个原告**的信息了，请问你是否需要继续添加**原告**信息？"
            json_data = json.dumps(st.session_state['yuangao_list'],ensure_ascii=False)
            print(json_data)
            json_data = json2md(json_data)
            res_answer= duo_yuangao+"现在的原告的json文件如下"+ json_data

            st.session_state['is_person']=True
            st.session_state['is_company']=True

    elif st.session_state['is_person']==False and st.session_state['is_company']==True:
        new_prompt_json={'role': 'user', 'content': gudie_yuangao_company_json+st.session_state["prompt2usr"]+st.session_state.prompt}
        res_json = api.main([new_prompt_json])
        print("-----------")
        print(res_json)
        print("-----------")
        data=extract_json_from_string(res_json)
        check_miss(data)
        if st.session_state['last_gen_keymiss']==st.session_state['gen_keymiss']:
            st.session_state['input_count']+=1
        else:
            st.session_state['input_count']=0
        if st.session_state['input_count']==3:
            st.session_state['input_count']=0
            for x in st.session_state['gen_keymiss']:
                st.session_state['yuangao_company_data'][x]="无"
            st.session_state['yuangao_list'].append(st.session_state['yuangao_company_data'])
            st.session_state['is_person']=True
            st.session_state['is_company']=True
            res_answer="亲，发现您多次没有提供有效的"+','.jion(st.session_state['gen_keymiss'])+"信息，先帮你跳过吧！我已经知道第"+str(len(st.session_state['yuangao_list']))+"个被告的信息了\n 请问你是否继续添加**原告**信息呢"
            return res_answer
        if len(st.session_state['gen_keymiss'])!=0:
            if "委托诉讼代理人" in st.session_state['gen_keymiss']:
                st.session_state['agent_flag_1'] = True
                res_answer="请问您是否有**委托代理人**？"
            else:
                res_answer="现在还不知道您的"+'，'.join(st.session_state['gen_keymiss'])+"信息，您能告诉我吗？"
        else:
            st.session_state['yuangao_list'].append(st.session_state['yuangao_company_data'])
            duo_yuangao="好的，我已经知道第"+str(len(st.session_state['yuangao_list']))+"个原告的信息了，请问你是否需要继续添加原告信息"
           
            json_data = json.dumps(st.session_state['yuangao_list'],ensure_ascii=False)
            json_data = json2md(json_data)
            res_answer= duo_yuangao+"现在的原告的json文件如下"+ json_data

            st.session_state['is_person']=True
            st.session_state['is_company']=True
    elif st.session_state['is_person']==True and st.session_state['is_company']==True:
        if judge_p_c(res_judge_jj_3):
            return "不好意思，没有听懂您的意思，请问你是否继续添加**原告**信息呢"
        elif (res_judge_no_2):
            res_json=2
        elif judge_p_c(res_judge_go_1):
            res_json=1
        else:
            return "不好意思，没有听懂您的意思，请问你是否继续添加**原告**信息呢"
        if res_json==1:
            res_answer="好的,我会继续为你添加**原告**信息,请问你还想添加**个人**还是**公司**呢？"
        else:
            st.session_state['second_state']=True
            res_answer="好的,我已经收集好了你的原告信息，麻烦您提供**被告人信息**，请问您的被告人是**个人**还是**公司**呢？"
        st.session_state['is_person']=False
        st.session_state['is_company']=False
    return res_answer

def on_input_change():

    if len(st.session_state.user_input)==0:
        # 这种对应的情况是无端的空白输入变化，将空白信息输出了
        return

    st.session_state['prompt'] = st.session_state['user_input']
    st.session_state['user_input'] = ''

    st.session_state['current_chat'].append({"role": "user", "content": st.session_state.prompt})

    if st.session_state['fourth_state']:
        res_answer=excute_fourth()
    elif st.session_state['third_state']:#第3步："案由", "诉讼请求", "事实理由", "证据", "日期"
        res_answer=excute_third()
    elif st.session_state['second_state']:#第2步：被告人信息
        res_answer=excute_second()
    else:                                 #第1步：原告人信息
        res_answer=excute_first()
    
    json2file(st.session_state['yuangao_list'],st.session_state['beigao_list'],st.session_state['third_state_data'])
    
    st.session_state['prompt2usr'] = res_answer
    msg = {'role':"assistant","content":res_answer}
    st.session_state['current_chat'].append(msg)


# ----------------------------- audio input -------------------------------------
st.session_state['user_input'] = ''
st.session_state['is_audio_input'] = False

if 'last_audio' not in st.session_state:
    st.session_state['last_audio'] = ''

placeholder = st.container()
with placeholder:
    start_button = Button(label='SPEAK', button_type='success', margin = (1, 1, 1, 1), width=200)

start_button.js_on_event("button_click", CustomJS(code=js_code))

audio_result = streamlit_bokeh_events(
    bokeh_plot = start_button,
    events="GET_TEXT,GET_ONREC,GET_INTRM",
    key="listen",
    refresh_on_update=False,
    override_height=30,
    debounce_time=500)


if audio_result:
    if "GET_ONREC" in audio_result and "GET_INTRM" in audio_result:
        if audio_result["GET_ONREC"] == 'stop' and audio_result["GET_INTRM"] =='':
            # print(st.session_state['last_audio'])
            # print(audio_result['GET_TEXT']['t'])
            if st.session_state['last_audio'] == audio_result['GET_TEXT']['t']:
                audio_result = None

# st.write(audio_result)
if audio_result:
    if 'GET_INTRM' in audio_result:
        st.write(audio_result['GET_INTRM'])
    
    if "GET_ONREC" in audio_result:
        if audio_result.get("GET_ONREC") == 'start':
            st.session_state['is_audio_input'] = True
    
        elif audio_result.get("GET_ONREC") == 'running':
            placeholder.image(os.path.join(project_path,'assert','sine_wave.gif'))
            st.session_state['is_audio_input'] = True
    
        elif audio_result.get("GET_ONREC") == 'stop':
            placeholder.image(os.path.join(project_path,'assert','end.jpg'))
            if 'GET_TEXT' in audio_result:
                st.session_state['user_input'] = audio_result['GET_TEXT']['t']
                st.session_state['last_audio'] = audio_result['GET_TEXT']['t']
                st.session_state['is_audio_input'] = False
                audio_result = None
                # print('here02 ： ',audio_result)
else:
    st.session_state['user_input'] = ''
# -------------------------------------------------------------------------------


st.text_area(label='输入区域，发送信息: ctl + enter, 语音输入自动识别停止',on_change=on_input_change,key='user_input')

if not st.session_state.is_audio_input:
    for i in range(len(st.session_state['current_chat'])-1,-1,-1):
        msg = st.session_state['current_chat'][i]
        message(msg['content'],is_user=(msg["role"]=='user'),key=st.session_state['message_keys'])
        if st.session_state["is_audio"] and msg["role"]!='user':
            # if msg["role"]!='user':
            wav_bytes = text2audio(msg['content'],os.path.join(project_path,'output','output.wav') )
            st.audio(wav_bytes, format="audio/wav", start_time=0)
        st.session_state['message_keys'] += 1

    
