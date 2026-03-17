from langgraph.graph import StateGraph, END
from graph.state import AgentState
from graph.nodes import call_model, call_tools

# 1. 创建图（蓝图）
workflow = StateGraph(AgentState)

# 2. 添加节点（工位）
workflow.add_node("agent", call_model)  # 大脑节点
workflow.add_node("tools", call_tools)  # 工具节点

# 3. 设置入口（从哪里开始？）
workflow.set_entry_point("agent")

# 4. 添加条件边（路由逻辑）
# 这是一个非常关键的函数：决定下一步去哪？
def should_continue(state):
    messages = state["messages"]
    last_message = messages[-1]
    
    # 如果大模型决定调用工具（有 tool_calls），就去 "tools" 节点
    if last_message.tool_calls:
        return "tools"
    # 否则（大模型直接回复了），就结束
    return END

# 添加这个条件边
workflow.add_conditional_edges(
    "agent",           # 从 agent 节点出来后
    should_continue,   # 执行这个判断函数
    {
        "tools": "tools",  # 如果函数返回 "tools"，就去 tools 节点
        END: END           # 如果函数返回 END，就结束
    }
)

# 5. 添加普通边（闭环）
# 工具执行完后，必须回给 agent，让它根据结果生成最终回复
workflow.add_edge("tools", "agent")

# 6. 编译图（把蓝图变成可运行的机器）
app = workflow.compile()