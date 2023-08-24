import json
import os
import sys

import pandas as pd
import streamlit as st

from scripts.json2docx import json2docx
from scripts.json2text import generate_docx
from utils.tools import (flatten_dictionary, generate_json_file,
                         unflatten_dataframe,get_project_path)

# with st.sidebar:
#     anthropic_api_key = st.text_input("Anthropic API Key", key="file_qa_api_key", type="password")
#     "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/1_File_Q%26A.py)"
#     "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"




st.title("📝 预览诉讼文书")

project_path = get_project_path()
json_file = os.path.join(project_path,'output','json_folder','person.json')
file_path = os.path.join(project_path,'output','docx_folder','legal_document.docx')


# 保存数据的函数，你可以根据需求进行自定义
def save_data(case_title, lawsuit_demands, factual_reasons, evidence):
    # 在这里执行保存逻辑，例如将数据保存到文件或数据库中
    pass

with open(json_file,'r',encoding='utf8') as f:
    json_data = json.load(f)

# 案由

st.subheader("案由")
case = st.text_input('当前的案由是', json_data["案由"])


# 原告
st.subheader("原告")

plaintiff = json_data["原告"]
plaintiff_df_list = []

for i in range(len(plaintiff)):
    st.markdown("###### 原告" + str(i+1))

    # 将嵌套的字典展开为新的键值对
    flattened_data = flatten_dictionary(plaintiff[i])

    # 将展开的键值对转换为 DataFrame
    df = pd.DataFrame([flattened_data])
    # df = df.transpose()
    plaintiff_df = st.data_editor(df, num_rows="fixed", key=str(i))
    plaintiff_df_list.append(plaintiff_df)


# 被告
st.subheader("被告")

defendant = json_data["被告"]
defendant_df_list = []

for i in range(len(defendant)):
    st.markdown("###### 被告" + str(i+1))

    # 将嵌套的字典展开为新的键值对
    flattened_data = flatten_dictionary(defendant[i])

    # 将展开的键值对转换为 DataFrame
    df = pd.DataFrame([flattened_data])
    # df = df.transpose()
    defendant_df = st.data_editor(df, num_rows="fixed", key=str(i+100))
    defendant_df_list.append(defendant_df)



# 诉讼请求文本编辑框
st.subheader("诉讼请求")
lawsuit_demands = st.text_area("请确认或修改诉讼文书的诉讼请求",value=json_data['诉讼请求'], height=500)

# 事实理由文本编辑框
st.subheader("事实理由")
factual_reasons = st.text_area("请确认或修改诉讼文书的事实理由",value=json_data['事实理由'], height=500)

# 证据文本编辑框
st.subheader("证据")
evidence = st.text_area("请确认或修改证据（如有）",value=json_data['证据'], height=300)

# 保存按钮
if st.button("保存"):
    # 在这里执行保存操作

    # 原告保存
    json_data['原告'] = []
    for i in range(len(plaintiff_df_list)):
        plaintiff_data = unflatten_dataframe(plaintiff_df_list[i])
        json_data['原告'].append(plaintiff_data)

    # 被告保存
    json_data['被告'] = []
    for i in range(len(defendant_df_list)):
        defendant_data = unflatten_dataframe(defendant_df_list[i])
        json_data['被告'].append(defendant_data)

    json_data['案由'] = case
    json_data['诉讼请求'] = lawsuit_demands
    json_data['事实理由'] = factual_reasons
    json_data['证据'] = evidence

    # 保存相关的json文件
    generate_json_file(json_data, json_file)
    
    # 保存对应的docx文件
    json2docx(json_data,file_path)
    st.success("保存成功！")

# 点击按钮进行下载
filename = os.path.basename(file_path)
with open(file_path, 'rb') as f:
    st.download_button('下载诉讼文书', f, file_name=filename)
