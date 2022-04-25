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

@app.get("/detail/{code_product}")
async def deatailProduct(code_product): # trả về danh sách infor của item
    pro = queryMongo.getDetailProduct(code_product)
    return {"detail_product": pro}

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
    print("read_item_query()")
    listProductInfo = queryMongo.getHotProduct()
    return {"list_item_infor": listProductInfo}

@app.get("/items/hotproduct")
async def read_item_query(): # trả về danh sách infor của item
    listProductInfo = queryMongo.getHotProduct()
    return {"list_item_infor": listProductInfo}

@app.get("/items/hotproduct")
async def read_item_query(id): # trả về danh sách infor của item
    listProductInfo = queryMongo.getHotProduct()
    return {"list_item_infor": listProductInfo}
@app.get("/items/related/{product_id}")
async def addRelated(product_id): # trả về danh sách infor của item
    queryMongo.addRelatedProduct(product_id)
    return {'true':"true"}
    
import service.RecommendService as rs

recommenderService = rs.RecommenderService()

@app.get("/v2/items")
async def read_item_query():
    return recommenderService.getAll()

@app.get("/v2/items/{id}")
async def read_item_query(id):
    return recommenderService.getOne(id)

@app.get("/v2/items/test/{id}")
async def read_item_query(id):
    return recommenderService.getOneTest(id)



@app.get("/v2/items/search/{query}")
async def read_item_query(query):
    return recommenderService.getOneTest(id)
