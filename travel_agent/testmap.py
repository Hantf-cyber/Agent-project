import requests
import json

# 1. 配置你的钥匙（高德 Web服务 Key）
# ⚠️ 注意：真实开发中，不要把 Key 直接写在代码里上传 GitHub，这里只是为了测试！
AMAP_KEY = "83fc9a76c8a78870217e77f86b3b39da"

def get_weather(city_code):
    """
    这是一个工具函数：查询天气
    """
    # 高德天气接口的网址
    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    
    # 打包要发送的数据
    params = {
        "key": AMAP_KEY,
        "city": city_code,  # 城市编码（比如北京是 110000）
        "extensions": "all" # all表示返回预报，base表示返回实况
    }
    
    # 发送请求（就像你在浏览器回车一样）
    print(f"正在向高德询问 {city_code} 的天气...")
    response = requests.get(url, params=params)
    
    # 把返回的 JSON 字符串变成 Python 字典
    data = response.json()
    return data

# --- 测试环节 ---
if __name__ == "__main__":
    # 北京的城市代码是 110000
    # 你可以去高德文档查其他城市的代码，或者暂时先用北京测
    weather_data = get_weather("110000")
    
    # 打印结果看看
    print("--- 高德返回的原始数据 ---")
    # indent=4 是为了让打印出来的 JSON 漂亮一点
    print(json.dumps(weather_data, indent=4, ensure_ascii=False))