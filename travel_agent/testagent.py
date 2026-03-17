from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
import sys

# 1. 强制设置路径（防止报错）
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from travel_agent.tools import get_weather

load_dotenv()

# 2. 召唤大脑
llm = ChatOpenAI(
    model="deepseek-chat",  # 或者是 glm-4
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),
    temperature=0.1  #稍微给点温度，让它灵活点
)

# 3. 强力绑定工具（注意这里加了一个 tool_choice="auto"）
# 这就像是把工具塞到它手里，告诉它“自动判断，该用就用”
llm_with_tools = llm.bind_tools([get_weather], tool_choice="auto")

def test_ai():
    print("--- 增强版测试：强制 AI 使用工具 ---")
    
    # 4. 构建对话历史（加上系统提示词 SystemMessage）
    # SystemMessage 就是给 AI 洗脑，设定人设
    messages = [
        SystemMessage(content="你是一个专业的旅行助手。如果用户询问天气，你必须调用 get_weather 工具获取实时数据，禁止自己编造。"),
        HumanMessage(content="帮我查一下北京（110000）现在的天气怎么样？")
    ]
    
    print(f"用户问题：{messages[1].content}")
    
    # 5. 让 AI 思考
    response = llm_with_tools.invoke(messages)
    
    print(f"\nAI 的回复对象：{response}")
    print(f"\nAI 是否决定调用工具：{response.tool_calls}")
    
    if response.tool_calls:
        print("\n🎉🎉🎉 成功了！AI 终于听话了！")
        tool_call = response.tool_calls[0]
        print(f"它要调用的函数：{tool_call['name']}")
        print(f"它提取的参数：{tool_call['args']}")
        
        # --- 这里是关键：我们真的去执行一下这个工具 ---
        # 真实开发中，这步由 LangGraph 自动完成，今天我们手动模拟一下
        print("\n--- 正在执行工具调用... ---")
        tool_result = get_weather.invoke(tool_call['args'])
        print(f"工具返回的真实结果：{tool_result}")
    else:
        print("\n😱 还是失败了... 它直接回答内容是：")
        print(response.content)

if __name__ == "__main__":
    test_ai()