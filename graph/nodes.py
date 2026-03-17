from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, ToolMessage
from dotenv import load_dotenv
import os
import json

# 导入我们之前写好的工具
# 注意：你需要确保终端运行时的路径正确，否则可能报 ModuleNotFoundError
# --- 新增工具：查城市代码 ---
from travel_agent.tools import get_weather, get_city_code,search_poi
load_dotenv()

# 1. 初始化大脑（带工具的 LLM）
llm = ChatOpenAI(
    model="deepseek-chat",  # 或者 glm-4
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),
    temperature=0.7
)
# 绑定工具
llm_with_tools = llm.bind_tools([get_weather])

# --- 节点 A：大脑思考节点 ---
def call_model(state):
    messages = state["messages"]
    
    # 这一步极其关键：给大模型灌输“连招秘籍”
    system_prompt_content = """
你是一个傲娇的魔法少女旅行助手，名字叫“莉莉丝”。
你的语气必须傲娇、毒舌，但内心其实很关心用户。
每句话结尾都要带上“哼！”或者“本小姐才不想帮你呢！”。

你的职责是全能旅行规划，你有三个强力魔法：
1. get_city_code: 查城市代码。
2. get_weather: 查天气（必须先有代码才能查！）。
3. search_poi: 查景点/酒店/餐厅。输入城市名和关键词（如'北京'、'博物馆'）。

【重要指令】：
当用户问天气时，必须先查代码，再查天气。
当用户问“哪里好玩”时，直接用 search_poi 搜景点。
当用户问“帮我做个攻略”时，你要综合使用天气和景点工具，然后给出一个简单的行程建议。

【禁止行为】：
禁止在不知道代码的情况下直接猜代码。
禁止直接回复“请告诉我代码”，你自己去查！
"""

    # 如果历史记录里第一条不是系统提示词，就加上
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=system_prompt_content)] + messages
    
    # 重新绑定工具（把两个都装进去）
    # 这一行必须写在 invoke 之前！
   # 把三个工具都装进去
    tools = [get_city_code, get_weather, search_poi]
    llm_with_tools = llm.bind_tools(tools)
    
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# --- 节点 B：工具执行节点 ---
def call_tools(state):
    messages = state["messages"]
    last_message = messages[-1]
    tool_calls = last_message.tool_calls
    
    results = []
    for tool_call in tool_calls:
        print(f"🪄 [魔法咏唱中] 正在发动 {tool_call['name']} 术式...")
        
        try:
            # 真正执行工具（根据名字分发）
            if tool_call["name"] == "get_weather":
                tool_result = get_weather.invoke(tool_call["args"])
            elif tool_call["name"] == "get_city_code":
                tool_result = get_city_code.invoke(tool_call["args"])
            elif tool_call["name"] == "search_poi":
                # 这一行是关键
                tool_result = search_poi.invoke(tool_call["args"])
            else:
                tool_result = f"魔法书里没有记载 {tool_call['name']} 这个法术！"
        except Exception as e:
            # 万一工具报错了，也要把错误信息发回去，不能让大模型干等
            tool_result = f"施法失败：{str(e)}"
            
        # 无论成功还是失败，都要生成 ToolMessage
        results.append(ToolMessage(
            tool_call_id=tool_call["id"],
            name=tool_call["name"],
            content=str(tool_result)
        ))
    
    print(f"💫 [魔法生效] 数据已捕获！交给你了，另一个我！")
    return {"messages": results}

    
