from pydantic import BaseModel, ValidationError

# 1. 给保安制定规则（定义数据模型）
class UserInfo(BaseModel):
    name: str      # str 表示必须是文本（字符串）
    age: int       # int 表示必须是整数
    is_vip: bool   # bool 表示必须是布尔值（True真 或 False假）

print("--- 测试 1：守规矩的好顾客 ---")
good_user = UserInfo(name="张三", age=25, is_vip=True)
print("通过校验的数据：", good_user)
print("这个人的名字是：", good_user.name)


print("\n--- 测试 2：乱填乱画的顾客 ---")
try:
    # 注意看！这里年龄故意填了文字 "二十"，VIP故意填了文字 "是"
    bad_user = UserInfo(name="李四", age="二十", is_vip="是")
except ValidationError as e:
    print("保安拦截成功！抓到了错误：")
    print(e)