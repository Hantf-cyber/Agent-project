from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from graph.graph_builder import app  # 导入我们做好的图
import uvicorn
import os
import sys

# 强制添加路径
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

# 1. 初始化 FastAPI
api = FastAPI(
    title="魔法少女莉莉丝 API",
    description="提供智能旅行规划服务的 RESTful 接口",
    version="1.0.0"
)

# 2. 定义请求的数据格式（Pydantic 又来了！）
class ChatRequest(BaseModel):
    query: str      # 用户的问题
    user_id: str = "default_user"  # 用户ID（用于区分不同人的对话历史，暂时先预留）

# 3. 定义响应的数据格式
class ChatResponse(BaseModel):
    response: str   # AI 的回答
    steps: list     # (可选) 展示一下 AI 的思考过程

# 4. 核心接口：聊天
@api.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        print(f"收到请求：{request.query}")
        
        # 构造输入消息
        inputs = {"messages": [HumanMessage(content=request.query)]}
        
        # 运行图（非流式，一次性拿结果）
        # invoke 和 stream 的区别是：invoke 等全部跑完才返回
        final_state = app.invoke(inputs)
        
        # 从最终状态里拿出最后一条 AI 的回复
        last_message = final_state["messages"][-1]
        
        return {
            "response": last_message.content,
            "steps": []  # 暂时留空
        }
        
    except Exception as e:
        print(f"出错啦：{str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 5. 启动入口
if __name__ == "__main__":
    uvicorn.run(api, host="127.0.0.1", port=8000)