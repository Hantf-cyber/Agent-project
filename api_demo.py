from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "你好！这是我的第一个 FastAPI 接口！"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "name": "神级装备"}