import streamlit as st

st.title("📝 用户反馈")

user_prompt = '我们非常重视您的反馈意见，请在以下输入框中提供您的宝贵意见。您的反馈将帮助我们改进产品和服务质量。谢谢！'

# 反馈意见输入框
feedback = st.text_area(user_prompt, height=150)

# 联系方式输入框
contact_info = st.text_input("请输入您的联系方式")

# 提交按钮
if st.button("提交"):
    # 在这里添加提交反馈逻辑
    st.write("反馈已提交！")

