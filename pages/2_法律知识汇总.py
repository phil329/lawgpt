
import json
import os
import sys

import streamlit as st

from utils.iflytek.Spark import Spark
from utils.prompt_config import knowledge_comment_prompt, related_result_prompt
from utils.tools import get_project_path

api = Spark()

st.title("🔎 相关法律知识")

# description = ' { "案由": "民间借贷纠纷", "诉讼请求": [ { "被告归还原告借款41,040元" }, { "被告支付原告违约金12,222元" }, { "被告承担本案诉讼费用" } ], "事实和理由": "原告冯雯与被告为朋友关系。被告在2018年1月19日向原告借款2万元，原告当天通过现金方式支付给被告。同日，被告再次向原告借款55,500元，并承诺在2018年4月29日前归还。原告分两次通过银行转账共计4万5千元以及500元现金给被告。此后，被告于2019年1月15日再次向原告借款1万元，原告当天通过现金方式支付给被告。自2018年至今，被告未按约定归还原告借款。原告多次催促被告还款，但被告仍未履行还款义务。因此，原告决定起诉被告，要求归还借款本金及支付违约金，并承担本案诉讼费用。", "证据": { "证据和证据来源": [ { "原告提供的银行转账记录、现金收据等证明被告借款的事实" }, { "原告与被告的聊天记录、通话录音等证明双方关于借款事宜的约定" } ] } }'

project_path = get_project_path()
json_file = os.path.join(project_path,'output','json_folder','person.json')


with open(json_file,'r') as f:
    description = f.read()


st.write(description)



# 创建两个列
left_column, right_column = st.columns(2)

with left_column:
    st.subheader('相关法律条款')
    chat_list = [{'role':'user','content':knowledge_comment_prompt+description}]
    res = api.main(chat_list)
    st.write(res)


with right_column:
    st.subheader('相关案例')
    chat_list = [{'role':'user','content':related_result_prompt+description}]
    res = api.main(chat_list)
    st.write(res)
