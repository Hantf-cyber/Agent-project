import operator
from typing import Annotated, List, TypedDict, Union
from langchain_core.messages import BaseMessage

# 定义我们的“共享内存”结构
class AgentState(TypedDict):
    # messages 是一个列表，里面存着所有的聊天记录（用户的问题、AI的思考、工具的结果）
    # Annotated[List[BaseMessage], operator.add] 的意思是：
    # 当有新消息来的时候，不要覆盖旧的，而是追加（add）到列表后面
    messages: Annotated[List[BaseMessage], operator.add]