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

# --- 新增工具：查城市代码 ---
@tool("get_city_code")
def get_city_code(city_name: str) -> str:
    """
    输入城市中文名称（如'北京'、'湘潭'），返回该城市的行政代码。
    """
    # 这里调用高德的【行政区域查询】接口
    url = "https://restapi.amap.com/v3/config/district"
    params = {
        "key": AMAP_KEY,
        "keywords": city_name,
        "subdistrict": 0  # 0表示不显示下级行政区，只要本级的
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # 如果查到了数据
        if data["status"] == "1" and len(data["districts"]) > 0:
            # 拿到第一个匹配结果的 adcode
            code = data["districts"][0]["adcode"]
            print(f"📜 [古老卷轴] 找到了！{city_name} 的真名代码是：{code}")
            return code
        else:
            return f"未找到 {city_name} 的代码，请检查城市名称是否正确。"
    except Exception as e:
        return f"查询出错：{str(e)}"
    
# --- 新增工具：搜周边景点 ---
@tool("search_poi")
def search_poi(city_name: str, keyword: str = "景点") -> str:
    """
    输入城市名（如'北京'）和关键词（如'博物馆'、'公园'），搜索相关地点。
    如果不填关键词，默认搜索'景点'。
    """
    url = "https://restapi.amap.com/v3/place/text"
    params = {
        "key": AMAP_KEY,
        "keywords": keyword,
        "city": city_name,
        "offset": 5,   # 只返回前5个结果，省点流量
        "page": 1,
        "extensions": "all"
    }
    try:
        print(f"🪄 [魔法咏唱中] 正在搜索 {city_name} 的 {keyword}...")
        response = requests.get(url, params=params)
        data = response.json()
        
        if data["status"] == "1" and int(data["count"]) > 0:
            pois = []
            for poi in data["pois"]:
                pois.append(f"- {poi['name']} ({poi['type']})")
            return f"在 {city_name} 找到了这些 {keyword}：\n" + "\n".join(pois)
        else:
            return f"呜呜...在 {city_name} 没找到关于 {keyword} 的地方。"
    except Exception as e:
        return f"魔法失效了：{str(e)}"