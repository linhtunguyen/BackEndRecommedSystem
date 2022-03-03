from fastapi import FastAPI #import class FastAPI() từ thư viện fastapi
import recomentest as recommending
import productTextEetrieval as recomendByQuery
app = FastAPI() # gọi constructor và gán vào biến app


@app.get("/") # giống flask, khai báo phương thức get và url
async def root(): # do dùng ASGI nên ở đây thêm async, nếu bên thứ 3 không hỗ trợ thì bỏ async đi
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id): # trả về danh sách id của item
    listPro= recommending.recommend(int(item_id),num=5)
    return {"list_item_id": listPro}

@app.get("/items/infor/{item_id}")
async def read_item(item_id): # trả về danh sách infor của item
    listPro=  recommending.getInforProductRecommended(recommending.recommend(int(item_id),num=5))
    return {"list_item_id": listPro}

@app.get("/items/query/{query_string}")
async def read_item(query_string: str): # trả về danh sách infor của item
    listPro= recomendByQuery.getProductItem(query_string)
    return {"list_item_id": listPro}

@app.get("/items/infor/query/{query_string}")
async def read_item(query_string: str): # trả về danh sách infor của item
    listPro= recommending.getInforProductRecommended(recomendByQuery.getProductItem(query_string))
    return {"list_item_id": listPro}