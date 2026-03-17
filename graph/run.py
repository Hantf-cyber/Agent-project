import sys
import os

# 强制添加路径（防止模块报错）
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from langchain_core.messages import HumanMessage
from graph.graph_builder import app

def main():
    print("✨ 傲娇魔法少女莉莉丝已上线！(输入 q 让本小姐退下)")
    
    while True:
        user_input = input("\n凡人(User): ")
        if user_input.lower() in ["q", "quit", "exit"]:
            print("👋 哼！本小姐去喝下午茶了，别想我！")
            break
        
        # 构造输入消息
        inputs = {"messages": [HumanMessage(content=user_input)]}
        
        # 运行图！
        print("🔮 莉莉丝正在翻阅魔法书...")
        for output in app.stream(inputs):
            for key, value in output.items():
                # 如果是 agent 节点，打印它的回复
                if key == "agent":
                    msg = value["messages"][-1]
                    if msg.content:
                        print(f"🎀 莉莉丝: {msg.content}")
        
        print("✨ 魔法施展完毕 ---")

if __name__ == "__main__":
    main()