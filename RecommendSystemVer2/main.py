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


@app.get("/items/hotproduct")
async def read_item_query(): # trả về danh sách infor của item
    print("read_item_query()")
    listProductInfo = queryMongo.getHotProduct()
    return {"list_item_infor": listProductInfo}

import service.RecommendService as rs

recommenderService = rs.RecommenderService()

@app.get("/v2/items")
async def v2_items():
    return recommenderService.getAll()

@app.get("/v2/items/{id}")
async def v2_item_id(id):
    return recommenderService.getOne(id)

@app.get("/v2/items/test/{id}")
async def v2_test(id):
    return recommenderService.getOneTest(id)

@app.get("/v2/items/search/{query}")
async def v2_items_search(query):
    return recommenderService.getProductByQuery(query)

@app.get("/v2/items/relative/{id}")
async def v2_items_search(id):
    return recommenderService.getItemRelative(id)

@app.get("/category/{categoryName}")
async def getProductOfCategory(categoryName):
    return {"listProduct":recommenderService.getListProductByCategory(categoryName)}

@app.get("/update/{categoryName}")
async def updateCategory(categoryNameOld, categoryNew):
    return recommenderService.updateCategory(categoryNameOld,categoryNew)