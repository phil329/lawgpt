import streamlit as st
from streamlit_chat import message
import sys

sys.path.append('/root/lawgpt')
from utils.prompt_config import start_chat,summary_chat_prompt
from utils.iflytek.Spark import Spark

api = Spark()


st.title("🦜 查看历史输入")
if 'current_chat' not in st.session_state:
    st.session_state['current_chat'] = [{"role": "assistant", "content": start_chat}]

if 'history_chat' not in st.session_state:
    st.session_state['history_chat'] = {}
    
    temp = st.session_state['current_chat']
    content = api._get_all_content(st.session_state['current_chat'])
    abstract = api.main([{'role':'user','content':summary_chat_prompt+content}])

    index = len(st.session_state['history_chat'])

    title = str(index)+'.'+abstract
    st.session_state['history_chat'][title] = temp

    
options = []
for chat in st.session_state['history_chat']:
    options.append(chat)
# 创建侧边栏
selection = st.sidebar.selectbox('Select an option', options)

print(selection)


for msg in st.session_state['history_chat'][selection]:
    # st.chat_message(msg["role"]).write(msg["content"])
    message(msg["content"],is_user=(msg["role"]=='user'))

