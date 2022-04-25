import pymongo
# import sys
# sys.path.append('/Content-based-Recommender-System-master/model/RecommendClicked.py')
# import RecommendClicked as recommending
import model.RecommendClicked as RecommendClicked
import model.TextRetrieval as TextRetrieval

myclient = pymongo.MongoClient("mongodb+srv://Hwuang:q@cluster0.ot4kn.mongodb.net/bigdata_project?retryWrites=true&w=majority")
mydb = myclient["ecommerce_electronic"]
mycolection = mydb["product"]




def recommendWhenClickToAProduct(item_id):
    listProductÌnfor = []
    recommending=RecommendClicked.SimilarityProduct()
    recommending.getSimilaryUseTfIdf()
    listProductCode = recommending.recommend(int(item_id), num=10)
    for proCode in listProductCode:
        result = mycolection.find_one({"code": proCode}, {'_id': 0})
        listProductÌnfor.append(result)
    return listProductÌnfor

recomendByQuery=TextRetrieval.Storage({})
item_descriptions = []
for i in TextRetrieval.items:
    item_descriptions.append(i)
recomendByQuery.fit_data(item_descriptions)

def recommendByQuery(query_string):
    result = {}
    # listProductÌnfor = []
    listProductCode = recomendByQuery.get_similiar_items(query_string)
    # for proCode in listProductCode:
    #     result = mycolection.find_one({"code": proCode}, {'_id': 0})
    #     listProductÌnfor.append(result)

    listProductInfor = list(mycolection.find({"code": { "$in": listProductCode }}, {'_id': 0}))
    # listProductInfor = []
    # for p in proCursor:
    #     listProductInfor.append(p)
    result["count"] = len(listProductInfor)
    result["listProduct"] = listProductInfor
    return result

def getDetail(id):
    print("getDetail, id = ", id)
    item = mycolection.find({'code': id})
    return item

def getHotProduct():
    listHotProduct=[]
    for product in mycolection.find({"rating": {"$gt": "3"}},{'_id': 0}).sort("ram"):
        listHotProduct.append(product)
    return listHotProduct

def getDetailProduct(prCode):
    return mycolection.find_one({"code": prCode}, {'_id': 0})

def addRelatedProduct(prCode):
    myquery = {"code": prCode}
    newvalues = {"$set": {"revalentItems": [1,2,3,4,5]}}
    mycolection.update_one(myquery, newvalues)
