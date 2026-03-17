from langchain.tools import tool
from pydantic import BaseModel, Field
import requests
import os
from dotenv import load_dotenv

# 1. 加载环境变量（从 .env 文件里读取 Key）
load_dotenv()
AMAP_KEY = os.getenv("AMAP_KEY")

# 2. 定义输入的格式（Pydantic 保安出场！）
class CityInput(BaseModel):
    """
    定义工具接收的参数结构
    Field(...) 里的 description 是写给大模型看的，告诉它这个参数是干嘛的
    """
    city_code: str = Field(description="城市的行政区划代码，例如北京是110000")

# 3. 定义工具函数（加上 @tool 装饰器）
@tool("get_weather", args_schema=CityInput)
def get_weather(city_code: str) -> str:
    """
    这是一个能够查询实时天气的工具。
    输入城市代码，返回该城市的天气情况。
    """
    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    params = {
        "key": AMAP_KEY,
        "city": city_code,
        "extensions": "all"
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data["status"] == "1":
            # 提取核心信息返回给大模型（省点 token）
            forecasts = data["forecasts"][0]["casts"]
            return f"查询成功！{data['forecasts'][0]['city']}未来几天的天气：{forecasts}"
        else:
            return f"查询失败：{data}"
    except Exception as e:
        return f"工具调用出错：{str(e)}"

# --- 测试环节 ---
if __name__ == "__main__":
    # 我们自己手动调一下试试
    print("--- 测试工具调用 ---")
    # 注意：真实调用时，参数是一个字典
    result = get_weather.invoke({"city_code": "110000"})
    print(result)