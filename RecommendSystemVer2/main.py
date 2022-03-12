from fastapi import FastAPI #import class FastAPI() từ thư viện fastapi
# from database.queryForRecommendProduct import *
import database.queryForRecommendProduct as queryMongo
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/items/testmongo/{item_id}")
async def read_item(item_id): # trả về danh sách infor của item
    listProductInfo= queryMongo.recommendWhenClickToAProduct(item_id)
    return {"list_item_infor": listProductInfo}

@app.get("/items/testmongo_query/{query_string}")
async def read_item_query(query_string: str): # trả về danh sách infor của item
    listProductInfo = queryMongo.recommendByQuery(query_string)
    # return {"list_item_infor": listProductInfo}
    return listProductInfo
@app.get("/items/hotproduct")
async def read_item_query(): # trả về danh sách infor của item
    listProductInfo = queryMongo.getHotProduct()
    return {"list_item_infor": listProductInfo}

@app.get("/items/hotproduct")
async def read_item_query(): # trả về danh sách infor của item
    listProductInfo = queryMongo.getHotProduct()
    return {"list_item_infor": listProductInfo}