import streamlit as st

# 初始文本内容
initial_text = "这是初始的文本内容"

# 在Streamlit应用程序中创建一个文本区域
text = st.text_area("文本区域", initial_text)

# 检查用户是否修改了文本内容
if text != initial_text:
    st.write("文本已经被修改！")

# 在需要的时候，可以使用新的文本内容进行更新
new_text = "这是新的文本内容"
st.text_area("文本区域", new_text)
