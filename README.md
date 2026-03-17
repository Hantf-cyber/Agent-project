# 🔮 魔法少女莉莉丝的旅行屋 (AI Agent Project)

> 一个基于 LangGraph + FastAPI + Streamlit 的多智能体旅行助手。
> 她性格傲娇，但能帮你查天气、搜景点、做攻略！

## ✨ 项目亮点
- **多 Agent 协作**：基于 LangGraph 构建 ReAct 智能体，包含搜索（Searcher）与规划（Planner）角色。
- **工具调用（Tools）**：集成高德地图 API，支持天气查询、POI 搜索、行政区划查询。
- **人设定制**：通过 System Prompt 打造“傲娇魔法少女”人设，提供沉浸式交互体验。
- **全栈开发**：
  - 后端：FastAPI 提供 RESTful 接口。
  - 前端：Streamlit 提供极简聊天界面。

## 🛠️ 技术栈
- **核心框架**：LangChain / LangGraph
- **大模型**：DeepSeek / ZhipuAI (GLM-4)
- **后端**：FastAPI / Uvicorn
- **前端**：Streamlit
- **工具**：高德地图 API

## 🚀 快速启动

### 1. 克隆项目
```bash
git clone https://github.com/Hantf-cyber/Agent-project.git
cd Agent-project