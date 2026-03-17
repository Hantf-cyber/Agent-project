import streamlit as st
import requests
import json
import time

# --- 页面配置 ---
st.set_page_config(
    page_title="魔法少女莉莉丝的旅行屋",
    page_icon="🔮",
    layout="centered"
)

# --- 自定义 CSS (让界面更漂亮) ---
# ⚠️ 注意这里！参数名改成了 unsafe_allow_html
st.markdown("""
<style>
    .stChatMessage {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .stChatMessage.user {
        background-color: #e6f7ff;
        text-align: right;
    }
    .stTitle {
        color: #ff6b6b;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# --- 标题与简介 ---
st.title("🔮 魔法少女莉莉丝的旅行屋")
st.caption("我是傲娇的莉莉丝，想去哪里玩？哼，才不想告诉你呢！(Powered by LangGraph)")

# --- 初始化聊天历史 ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # 开场白
    st.session_state.messages.append({
        "role": "assistant",
        "content": "哼！凡人，你终于来了？想去哪玩？快说，本小姐的时间可是很宝贵的！"
    })

# --- 展示聊天记录 ---
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🔮" if message["role"] == "assistant" else "🧑‍💻"):
        st.markdown(message["content"])

# --- 处理用户输入 ---
if prompt := st.chat_input("输入你的旅行计划..."):
    # 1. 展示用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    # 2. 调用后端 API (server.py)
    with st.chat_message("assistant", avatar="🔮"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # 显示思考中的状态
            with st.spinner("🔮 莉莉丝正在翻阅魔法书..."):
                # 发送请求给 FastAPI
                response = requests.post(
                    "http://127.0.0.1:8000/chat",
                    json={"query": prompt, "user_id": "streamlit_user"},
                    timeout=60  # 设置超时时间
                )
                
                if response.status_code == 200:
                    data = response.json()
                    full_response = data["response"]
                    
                    # 模拟打字机效果
                    displayed_response = ""
                    for chunk in full_response.split():
                        displayed_response += chunk + " "
                        message_placeholder.markdown(displayed_response + "▌")
                        time.sleep(0.05)
                    message_placeholder.markdown(full_response)
                else:
                    st.error(f"魔法失效了！错误代码：{response.status_code}")
                    full_response = "呜呜...魔法书打不开了。"
        except Exception as e:
            st.error(f"无法连接到魔法屋：{str(e)}")
            full_response = "后端服务没启动吧？笨蛋！快去运行 python server.py！"
            
    # 3. 保存 AI 回复到历史
    st.session_state.messages.append({"role": "assistant", "content": full_response})